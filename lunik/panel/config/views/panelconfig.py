# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime

from user_sessions.models import Session
from panel.core.decorators import access_for_superuser, ajax_required
from panel.core.utils import user_logs,delete_record
from panel.config.models import PanelAdmin
from panel.config.forms import PanelAdminForm
from panel.accounts.models import User

# Create your views here.
@access_for_superuser
def panel_list(request):
    context = {}

    context['panel_list'] = PanelAdmin.objects.order_by('title')

    return render(request,'config/panel_list.html',context)

@access_for_superuser
def panel_add(request):
    context = {}

    if request.method == 'POST':
        context['form'] = PanelAdminForm(request.POST,request.FILES)
        
        if context['form'].is_valid():
            context['form'].save()
			
            #-- Message to user
            messages.success(request, 'Datos del panel creado satisfactoriamente')

			#-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Dato del panel creado satisfactoriamente')

            return redirect('config:panel_list')
    else:
        context['form'] = PanelAdminForm()

    return render(request, 'config/panel_form.html', context)

@access_for_superuser
def panel_edit(request,pk):
    context = {}

    context['instance'] = get_object_or_404(PanelAdmin, pk=pk)

    if request.method == 'POST':
        context['form'] = PanelAdminForm(request.POST, request.FILES,instance=context['instance'])
        
        if context['form'].is_valid():
            context['form'].save()
			
            #-- Message to user
            messages.success(request, 'Datos del panel modificado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Datos del panel modificado satisfactoriamente')

            return redirect('config:panel_list')
    else:
        context['form'] = PanelAdminForm(instance=context['instance'])

    return render(request, 'config/panel_form.html', context)

@access_for_superuser
def sessions_list(request):
    context = {}
    
    context['sessions_list'] = Session.objects.filter(expire_date__gt=datetime.now()).exclude(user__isnull=True)\
                               .order_by('-last_activity')

    return render(request,'config/sessions_list.html',context)

@access_for_superuser
def sessions_delete(request,pk):

    session = get_object_or_404(Session,pk=pk)

    session.delete()

    #-- Message to user
    messages.success(request, 'Sesión de usuario cerrada satisfactoriamente')

    #-- User Logs (Info, Access, Error)
    user_logs(request,None,'A','Sesión de usuario cerrada satisfactoriamente')

    return redirect('/panel/config/account/sessions/')

