# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse

from panel.core.utils import delete_record
from panel.website.models import Faq
from panel.website.forms import FaqForm

# Create your views here.
def faqs_list(request):
    context = {}

    context['faqs_list'] = Faq.objects.filter(status=True).order_by('-created')

    return render(request,'website/faqs_list.html',context)

def faqs_add(request):
    context = {}

    if request.method == 'POST':
        context['faq_form'] = FaqForm(request.POST)

        if context['faq_form'].is_valid():
            context['faq_form'].save()

            return redirect('website:faqs_list')

    else:
        context['faq_form'] = FaqForm()

    return render(request,'website/faqs_form.html',context)

def faqs_edit(request,pk):
    context = {}

    context['faq_obj'] = get_object_or_404(Faq,pk=pk)

    if request.method == 'POST':
        context['faq_form'] = FaqForm(request.POST,instance=context['faq_obj'])

        if context['faq_form'].is_valid():
            context['faq_form'].save()

            return redirect('website:faqs_list')

    else:
        context['faq_form'] = FaqForm(instance=context['faq_obj'])

    return render(request,'website/faqs_form.html',context)

def faqs_delete(request,pk):
    context = {}

    faq = get_object_or_404(Faq, pk=pk)

    data = delete_record(request,faq,'/panel/website/faqs/','website:faqs_delete')

    return JsonResponse(data)	
