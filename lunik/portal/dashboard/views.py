# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

from panel.core.decorators import access_for_customer
from panel.core.utils import user_logs, pagination, tenant_from_request
from panel.accounts.models import User, Customer
from panel.website.models import StoreMeta
from portal.dashboard.forms import UserProfileForm, ChangePasswordForm
from portal.shop.models import ShopOrder
from portal.dashboard.models import Address
from portal.dashboard.forms import AddressForm
# Create your views here.
@access_for_customer
def profile(request):
	context = {}
	tenant = tenant_from_request(request)
	context['orders'] = ShopOrder.objects.filter(customer=request.user).select_related('order_payment', 'shop_order_delivery').order_by('-created')[:3]
	context['count_orders'] = ShopOrder.objects.filter(customer=request.user)
	context['addresses'] = Address.objects.filter(user=request.user, store_meta__store__customer__tenant=tenant).order_by('-default')[:3]
	return render(request, 'dashboard/profile/profile.html', context)

@access_for_customer
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

@access_for_customer
def orders(request):
	context = {}
	orders = ShopOrder.objects.filter(customer=request.user).select_related('order_payment', 'shop_order_delivery').order_by('-created')
	page = request.GET.get('page', 1)
	context['orders'] = pagination(orders, page, 6)
	return render(request, 'dashboard/orders/orders_list.html', context)

def get_order(request, pk):
	context = {}
	data = {}

	context['order'] = get_object_or_404(ShopOrder, pk=pk)
	customer = get_object_or_404(Customer.objects.prefetch_related('shop_orders'), shop_orders=context['order'])
	context['customer'] = get_object_or_404(User, email=request.user.email, customer__pk=customer.pk, is_customer=True)
	if request.is_ajax() and request.method == 'GET':
		data['html_order'] = render_to_string('dashboard/orders/includes/partial_order.html',context, request=request)
	else:
		data['form_is_valid'] = False

	return JsonResponse(data)

@access_for_customer
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

@access_for_customer
def address(request):
	context = {}
	tenant = tenant_from_request(request)
	context['addresses'] = Address.objects.filter(user=request.user, store_meta__store__customer__tenant=tenant)
	return render(request, 'dashboard/address/list.html', context)


@access_for_customer
def add_address(request):
	context = {}
	tenant = tenant_from_request(request)
	store_meta = get_object_or_404(StoreMeta, store__customer__tenant=tenant)
	if request.method == 'POST':
		context['form'] = AddressForm(request.POST, request=request)
		if context['form'].is_valid():
			if context['form'].cleaned_data['default']:
				try:
					obj = Address.objects.get(default=True, user=request.user, store_meta__store__customer__tenant=tenant)
					obj.default = False
					obj.save()
				except Address.DoesNotExist:
					pass

			form = context['form'].save(commit=False)
			form.user = request.user
			form.store_meta = store_meta
			form.save()
			return redirect('dashboard:address')
	else:
		context['form'] = AddressForm(request=request)
	return render(request, 'dashboard/address/form.html', context)


@access_for_customer
def edit_address(request, pk):
	context = {}
	tenant = tenant_from_request(request)
	context['address_obj'] = get_object_or_404(Address, pk=pk)
	if request.method == 'POST':
		context['form'] = AddressForm(request.POST, instance=context['address_obj'], request=request)
		if context['form'].is_valid():
			if context['form'].cleaned_data['default']:
				obj = Address.objects.get(default=True, user=request.user, store_meta__store__customer__tenant=tenant)
				obj.default = False
				obj.save()
			form = context['form'].save()
			return redirect('dashboard:address')
	else:
		context['form'] = AddressForm(instance=context['address_obj'], request=request)
	return render(request, 'dashboard/address/form.html', context)
