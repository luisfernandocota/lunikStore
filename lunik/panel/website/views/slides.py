# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib import messages

from panel.core.utils import delete_item
from panel.website.models import Slide
from panel.website.forms import SlideForm


def slides_list(request):
    context = {}
    context['slides_list'] = Slide.objects.filter(status=True).order_by('title')

    return render(request,'website/slides_list.html',context)

def slides_add(request):
    context = {}

    if request.method == 'POST':
        if request.FILES:
            print('hola')
        else:
            print('nada')
        # files=request.FILES
        # i = 0
        # for obj in files:
        #     i += 1
        #     Slide.objects.create(image=files[obj])
        # messages.success(request, 'Han sido agregado(s) %s slide(s) correctamente' %(i))
        # return redirect('website:slides_list')

    else:
        context['slide_form'] = SlideForm()

    return render(request,'website/slides_form.html',context)

def slides_edit(request,pk):
    context = {}
    data = {}

    context['slide_obj'] = Slide.objects.get(pk=pk)
    
    if request.is_ajax() and request.method == 'POST':
        context['slide_form'] = SlideForm(request.POST,request.FILES,instance=context['slide_obj'])

        if context['slide_form'].is_valid():
            context['slide_form'].save()

            data['form_is_valid'] = True
            messages.success(request, 'Slide editado correctamente')

        else:
            data['form_is_valid'] = False
            data['html_failed'] = render_to_string('core/snippets/success_modal.html', context, request=request)
    else:
        context['name_form'] = 'Editar slide'
        context['url_post'] = '/panel/website/slides/edit/%s/' % context['slide_obj'].pk
        context['slide_form'] = SlideForm(instance=context['slide_obj'])
        data['html_form'] = render_to_string('website/modals/slides_edit.html', context, request)

    return JsonResponse(data)

def slides_delete(request,pk):
    context = {}
    data = {}

    slide = get_object_or_404(Slide, pk=pk)

    data = delete_item(request,slide, '/panel/website/slides/', '/panel/website/slides/delete/','Slide eliminado')

    return JsonResponse(data)
