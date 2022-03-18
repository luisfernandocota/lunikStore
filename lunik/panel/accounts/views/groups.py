# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from panel.core.decorators import debugger_queries

from panel.core.utils import user_logs,delete_record
from panel.accounts.models import User,Role,UserModuleGroup
from panel.accounts.forms import UserModuleGroupForm

# Create your views here.
def usergroups_list(request):
    context = {}

    context['groups_list'] = Role.objects.prefetch_related('group').order_by('name')

    #context['groups_list'] = UserMenuGroup.objects.values('user_type__pk','user_type__name').annotate(total=Count('menu_item')).\
    #                         filter(status=True).order_by('user_type__name')

    return render(request,'accounts/groups_list.html',context)

@debugger_queries
def usergroups_add(request):
    context = {}

    #-- List of menu modules
    context['menu_list'] = User.modules_list()

    if request.method == 'POST':
        context['form'] = UserModuleGroupForm(request.POST)

        if context['form'].is_valid():

            User.save_modules_group(request.POST.getlist('modules_group'),context['form'],False)

            #-- Message to user
            messages.success(request, 'Grupo de usuario creado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Grupo de usuario creado satisfactoriamente')

            return redirect('accounts:usergroups_list')
    else:
        context['form'] = UserModuleGroupForm()

    return render(request, 'accounts/groups_form.html', context)

def usergroups_edit(request,pk):
    context = {}

    context['instance'] = UserModuleGroup.objects.filter(role__pk=pk)

    #-- List of menu modules
    context['menu_list'] = User.modules_list()

    if request.method == 'POST':
        context['form'] = UserModuleGroupForm(request.POST, instance=context['instance'].first())

        if context['form'].is_valid():

            User.save_modules_group(request.POST.getlist('modules_group'),context['form'],True)

            #-- Message to user
            messages.success(request, 'Grupo de usuario modificado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Grupo de usuario modificado satisfactoriamente')

            return redirect('accounts:usergroups_list')
    else:
        context['form'] = UserModuleGroupForm(instance=context['instance'].first())

    return render(request, 'accounts/groups_form.html', context)

def usergroups_delete(request,pk):

    context = {}
    data = {}

    context['role'] = get_object_or_404(Role,pk=pk)

    if request.is_ajax and request.method == 'POST':

      #-- Delete group permissions
      UserModuleGroup.objects.filter(role=context['role']).delete()

      #-- Delete relations users with group
      context['role'].user.clear()

      messages.success(request, 'Registro eliminado satisfactoriamente')

      #-- User Logs (Info, Access, Error)
      user_logs(request,None,'A','Registro eliminado satisfactoriamente')

      data['form_is_valid'] = True
      data['url_redirect'] = '/panel/accounts/usergroups/'
      data['message'] = 'Registro eliminado satisfactoriamente'

    else:

      context['obj_delete'] = context['role']
      context['url_post'] = 'accounts:usergroups_delete'

      data['html_form'] = render_to_string('core/snippets/modal_delete.html', context, request=request)

    return JsonResponse(data)
