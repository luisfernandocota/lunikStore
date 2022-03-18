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
from panel.config.forms import TemplateComponentForm
from panel.config.models import TemplateComponent

# Create your views here.
@access_for_superuser
def component_list(request):
    context = {}

    context['components_list'] = TemplateComponent.objects.filter(status=True).order_by('name')

    return render(request,'config/components_list.html',context)

@access_for_superuser
def component_add(request):
    context = {}

    if request.method == 'POST':
        context['component_form'] = TemplateComponentForm(request.POST)
        if context['component_form'].is_valid():
            context['component_form'].save(commit=False)
            context['component_form'].code = request.POST.get('code')
            context['component_form'].save()
            #-- Message to user
            messages.success(request, 'Componente creado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Componente creado satisfactoriamente')

            return redirect('config:component_list')
    else:
        context['component_form'] = TemplateComponentForm()

    return render(request, 'config/components_form.html', context)

@access_for_superuser
def component_edit(request,pk):
    context = {}

    context['instance'] = get_object_or_404(TemplateComponent, pk=pk)

    if request.method == 'POST':
        context['component_form'] = TemplateComponentForm(request.POST, instance=context['instance'])

        if context['component_form'].is_valid():
            context['component_form'].save()

            #-- Message to user
            messages.success(request, 'Componente modificado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Componente modificado satisfactoriamente')

            return redirect('config:component_list')
    else:

        context['component_form'] = TemplateComponentForm(instance=context['instance'])

    return render(request, 'config/components_form.html', context)

@access_for_superuser
def component_delete(request,pk):

	menu = get_object_or_404(ModuleItem, pk=pk)

	data = delete_record(request,menu,reverse('config:component_list'),reverse('config:component_delete',kwargs={'pk':pk}))

	#-- User Logs (Info, Access, Error)
	user_logs(request,None,'I','Componente eliminado satisfactoriamente')

	return JsonResponse(data)

def component(request, pk):
    context = {}
    context['component'] = get_object_or_404(TemplateComponent, pk=pk)

    return render(request, 'config/includes/component.html', context)
