# -*- coding: utf-8 -*-
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F

from panel.core.decorators import access_for_superuser
from panel.accounts.models import Role, User
from panel.core.utils import user_logs,delete_record
from panel.config.forms import ModuleItemForm, ModuleSubItemForm
from panel.config.models import ModuleItem, ModuleSubItem

# Create your views here.
@access_for_superuser
def menu_list(request):
    context = {}

    context['menu_list'] = ModuleItem.objects.filter(status=True).order_by('title')

    return render(request,'config/menu_list.html',context)

@access_for_superuser
def menu_add(request):
    context = {}

    if request.method == 'POST':
        context['menu_form'] = ModuleItemForm(request.POST)

        if context['menu_form'].is_valid():
            context['menu_form'].save()

            #-- Message to user
            messages.success(request, 'Menú creado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Menú creado satisfactoriamente')

            return redirect('config:menu_list')
    else:
        context['menu_form'] = ModuleItemForm()

    return render(request, 'config/menu_form.html', context)

@access_for_superuser
def menu_edit(request,pk):
    context = {}

    context['menu_obj'] = get_object_or_404(ModuleItem, pk=pk)

    if request.method == 'POST':
        context['menu_form'] = ModuleItemForm(request.POST, instance=context['menu_obj'])

        if context['menu_form'].is_valid():
            context['menu_form'].save()

            #-- Message to user
            messages.success(request, 'Menú modificado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Menú modificado satisfactoriamente')

            return redirect('config:menu_list')
    else:

        context['menu_form'] = ModuleItemForm(instance=context['menu_obj'])

    return render(request, 'config/menu_form.html', context)

@access_for_superuser
def menu_delete(request,pk):
    menu = get_object_or_404(ModuleItem, pk=pk)
    #-- Before
    #data = delete_record(request,menu,reverse('config:menu_list'),reverse('config:menu_delete',kwargs={'pk':pk}))
    #-- After
    data = delete_record(request,menu,reverse('config:menu_list'), '/panel/config/menu/delete/%s' %(menu.pk))
    
    #-- Delete Submenu Items
    if data:
        ModuleSubItem.objects.filter(item=menu).update(status=False)
        
        #-- Delete Module´s User
        User.delete_modules_user(menu)
        
    
    #-- User Logs (Info, Access, Error)
    user_logs(request,None,'I','Registro eliminado satisfactoriamente')
    
    return JsonResponse(data)

# Create your views here.
@access_for_superuser
def submenu_list(request):
    context = {}

    context['submenu_list'] = ModuleSubItem.objects.select_related('item').filter(status=True).order_by('item__title','title')

    return render(request,'config/submenu_list.html',context)

@access_for_superuser
def submenu_add(request):
    context = {}

    if request.method == 'POST':
        context['submenu_form'] = ModuleSubItemForm(request.POST)

        if context['submenu_form'].is_valid():
            context['submenu_form'].save()

            #-- Message to user
            messages.success(request, 'submenu creado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','submenu creado satisfactoriamente')

            return redirect('config:submenu_list')
    else:
        context['submenu_form'] = ModuleSubItemForm()

    return render(request, 'config/submenu_form.html', context)

@access_for_superuser
def submenu_edit(request,pk):
    context = {}

    context['submenu_obj'] = get_object_or_404(ModuleSubItem, pk=pk)

    if request.method == 'POST':
        context['submenu_form'] = ModuleSubItemForm(request.POST, instance=context['submenu_obj'])

        if context['submenu_form'].is_valid():
            context['submenu_form'].save()

            #-- Message to user
            messages.success(request, 'submenu modificado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','submenu modificado satisfactoriamente')

            return redirect('config:submenu_list')
    else:

        context['submenu_form'] = ModuleSubItemForm(instance=context['submenu_obj'])

    return render(request, 'config/submenu_form.html', context)

@access_for_superuser
def submenu_delete(request,pk):

	submenu = get_object_or_404(ModuleSubItem, pk=pk)

	data = delete_record(request,submenu,reverse('config:submenu_list'),reverse('config:submenu_delete',kwargs={'pk':pk}))

	#-- Delete Submenu Items
	if data:
		#-- Delete SubModule´s User
		User.delete_submodules_user(submenu)

	#-- User Logs (Info, Access, Error)
	user_logs(request,None,'I','submenu eliminado satisfactoriamente')

	return JsonResponse(data)
