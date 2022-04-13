# -*- coding: utf-8 -*-
import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

import pgeocode

from panel.core.decorators import access_for_customer
from panel.core.utils import user_logs, pagination
from panel.accounts.models import User
from portal.dashboard.forms import UserProfileForm, ChangePasswordForm
from portal.shop.models import ShopOrder
from portal.dashboard.models import Address
from portal.dashboard.forms import AddressForm
# Create your views here.
def profile(request):
	context = {}
	context['orders'] = ShopOrder.objects.filter(customer=request.user).select_related('order_payment', 'shop_order_delivery').order_by('-created')[:3]
	context['count_orders'] = ShopOrder.objects.filter(customer=request.user)
	context['addresses'] = Address.objects.filter(user=request.user).order_by('-default')[:3]
	return render(request, 'dashboard/profile/profile.html', context)

def edit_profile(request):
	context = {}

	if request.method == 'POST':
		context['form'] = UserProfileForm(request.POST, request.FILES, instance=request.user,\
											user=request.user)

		if context['form'].is_valid():
			profile_save = context['form'].save()

			msg = messages.success(request, 'Perfil modificado satisfactoriamente')

			#-- User Logs (Info, Access, Error)
			user_logs(request,None,'I','Perfil modificado satisfactoriamente')

			return redirect('dashboard:profile')
	else:

		context['form'] = UserProfileForm(instance=request.user, user=request.user)

	return render(request, 'dashboard/profile/edit_profile.html', context)

def orders(request):
	context = {}
	orders = ShopOrder.objects.filter(customer=request.user).select_related('order_payment', 'shop_order_delivery').order_by('-created')
	page = request.GET.get('page', 1)
	context['orders'] = pagination(orders, page, 6)
	return render(request, 'dashboard/orders/orders_list.html', context)

def order_detail(request, pk):
	context = {}
	data = {}

	context['order'] = get_object_or_404(ShopOrder, pk=pk)
	context['customer'] = get_object_or_404(User, email=request.user.email, is_customer=True)

	return render(request, 'dashboard/orders/order_detail.html', context)


def password_edit(request):
	context = {}

	if request.method == 'POST':
		context['form'] = ChangePasswordForm(request.POST, user=request.user)

		if context['form'].is_valid():

			password = context['form'].cleaned_data['password']

			request.user.set_password(password)

			request.user.save()

			update_session_auth_hash(request, request.user)

			msg = messages.success(request, 'Contraseña modificada satisfactoriamente')
			#-- User Logs (Info, Access, Error)
			user_logs(request,None,'I','Contraseña modificada satisfactoriamente')

			return redirect('dashboard:profile')

	else:
		context['form'] = ChangePasswordForm(user=request.user)

	return render(request, 'dashboard/profile/password_form.html', context)

def address(request):
	context = {}
	context['addresses'] = Address.objects.filter(user=request.user)
	return render(request, 'dashboard/address/list.html', context)


def add_address(request):
	context = {}
	if request.method == 'POST':
		context['form'] = AddressForm(request.POST, request=request)
		if context['form'].is_valid():
			if context['form'].cleaned_data['default']:
				try:
					obj = Address.objects.get(default=True, user=request.user)
					obj.default = False
					obj.save()
				except Address.DoesNotExist:
					pass

			form = context['form'].save(commit=False)
			form.user = request.user
			form.save()
			return redirect('dashboard:address')
	else:
		context['form'] = AddressForm(request=request)
	return render(request, 'dashboard/address/form.html', context)


def edit_address(request, pk):
	context = {}
	context['address_obj'] = get_object_or_404(Address, pk=pk)
	if request.method == 'POST':
		context['form'] = AddressForm(request.POST, instance=context['address_obj'], request=request)
		if context['form'].is_valid():
			if context['form'].cleaned_data['default']:
				obj = Address.objects.get(default=True, user=request.user)
				obj.default = False
				obj.save()
			form = context['form'].save()
			return redirect('dashboard:address')
	else:
		context['form'] = AddressForm(instance=context['address_obj'], request=request)
	return render(request, 'dashboard/address/form.html', context)

def get_zip_code(request):
	data = {}

	data = {'state':'', 'county':'', 'community':'', 'suburbs':{}}
	pgeocode.DOWNLOAD_URL = [os.environ.get("PGEOCODEURLS")]
	geocode = pgeocode.Nominatim('mx')
	addressInfo = geocode.query_postal_code(request.GET.get("zipcode"))
	data['state'] = addressInfo.state_name
	data['county'] = addressInfo.county_name
	data['community'] = addressInfo.community_name

	list_address = [i.lstrip() for i in str(addressInfo.place_name).split(',')]

	data['suburbs'] = list_address

	return JsonResponse(data)