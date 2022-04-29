# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse


from panel.core.utils import pagination
from panel.accounts.models import User
from panel.website.forms import SearchCustomerForm

def customers_list(request):
    context = {}
    data = {}
    if request.is_ajax() and request.method == 'GET':
        context['form_search'] = SearchCustomerForm(request.GET)
        if context['form_search'].is_valid():
            query = context['form_search'].cleaned_data['query']
            if query and query is not None:
                lookups = Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)
                customers_list = User.objects.filter(is_customer=True, is_active=True, is_superadmin=False).filter(lookups)
                if customers_list.exists():
                    page = request.GET.get('page',1)
                    context['customers_list'] = pagination(customers_list,page,20)
                    data['search_valid'] = True
                    data['html_orders'] = render_to_string('website/customers/includes/partial_customers_list.html', context, request=request)
                else:
                    data['search_valid'] = False
                    data['message'] = 'Orden no encontrada'
                
                return JsonResponse(data)
                



    page = request.GET.get('page',1)
    customers_list = User.objects.filter(is_customer=True, is_active=True, is_superadmin=False)
    context['form_search'] = SearchCustomerForm()
    context['customers_list'] = pagination(customers_list,page,20)

    return render(request,'website/customers/customers_list.html',context)
