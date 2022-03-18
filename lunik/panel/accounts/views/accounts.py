# -*- coding: utf-8 -*-
import datetime

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

from panel.core.utils import user_logs,delete_record,sendmail_activation_record
from panel.core.decorators import access_for_user

from panel.config.models import Logger
from panel.accounts.models import User,Role,UserModulePermission
from panel.accounts.forms import UserForm

def accounts_list(request):
	context = {}
	context['user_list'] = User.objects.select_related('role').filter(status=True).exclude(is_superuser=True)

	return render(request, 'accounts/accounts_list.html', context)

def accounts_add(request):
	context = {}

	#-- List of menu modules
	context['menu_list'] = User.modules_list()
	if request.method == 'POST':
		context['form'] = UserForm(request.POST,request.FILES,user=request.user)
		if context['form'].is_valid():

			user = context['form'].save(commit=False)
			password = get_random_string(10)


			user.role = Role.objects.get(status=True, name__iexact='Administrador')
			user.set_password(password)
			user.save()

			role = context['form'].cleaned_data['role']

			#-- If user role is a group
			if role.is_group:
				#-- Save relation User/ Group
				role.user.add(user)
			else:
				User.save_modules_list(request.POST.getlist('modules_user'),user,False)

			#-- Call static method
			User.activation_email(request,user,password)

			#-- Message to user
			messages.success(request, 'Usuario creado satisfactoriamente')

			#-- User Logs (Info, Access, Error)
			user_logs(request,None,'I','Usuario creado satisfactoriamente')

			return redirect('accounts:accounts_list')
	else:

		context['form'] = UserForm(user=request.user)

	return render(request, 'accounts/accounts_form.html', context)

@access_for_user
def accounts_edit(request, pk):

	context = {}
	
	context['user_profile'] = get_object_or_404(User, pk=pk)

	current_usertype = context['user_profile'].role
	
	#-- List of menu modules
	context['menu_list'] = User.modules_list()

	if request.method == 'POST':
		context['form'] = UserForm(request.POST, request.FILES, instance=context['user_profile'],\
											user=context['user_profile'])

		if context['form'].is_valid():

			#-- If user is in group
			user_role = context['form'].cleaned_data['role']

			if user_role.is_group:
				UserModulePermission.objects.filter(user=context['user_profile']).delete()
				context['user_profile'].user_groups.remove(current_usertype)
				user_role.user.add(context['user_profile'])
			else:
				context['user_profile'].user_groups.remove(current_usertype)
				User.save_modules_list(request.POST.getlist('modules_user'),context['user_profile'],True)

			context['form'].save()

			messages.success(request, 'Usuario modificado satisfactoriamente')

			#-- User Logs (Info, Access, Error)
			user_logs(request,None,'I','Usuario modificado satisfactoriamente')

			return redirect('accounts:accounts_list')
	else:
		
		#-- Get User Role
		if context['user_profile'].role.is_group:
			context['usertype_select'] = 'true'
		else:
			context['usertype_select'] = 'false'

		context['form'] = UserForm(instance=context['user_profile'], user=context['user_profile'])
	
	return render(request, 'accounts/accounts_form.html', context)

def accounts_delete(request, pk):

	user = get_object_or_404(User, pk=pk)

	data = delete_record(request,user,reverse('accounts:accounts_list'),reverse('accounts:accounts_delete',kwargs={'pk':pk}))

	return JsonResponse(data)

def accounts_sendmail_activation(request, pk):

	user = get_object_or_404(User, pk=pk)

	password = get_random_string(10)
	user.set_password(password)
	user.save()

	data = sendmail_activation_record(request,user,password,reverse('accounts:accounts_list'),reverse('accounts:accounts_sendmail_activation',kwargs={'pk':pk}))

	return JsonResponse(data)

def accounts_activation(request, uidb64, token):

	user_activation = User.activation_url(uidb64,token)

	if user_activation:

		#-- User Logs (Info, Access, Error)
		user_logs(request,user_activation,'A','Usuario activado satisfactoriamente')

		return render(request, 'accounts/accounts_activation.html')
	else:
		return render(request, 'accounts/accounts_expire.html')

def accounts_logs(request,pk):
	context = {}

	user = get_object_or_404(User, pk=pk)

	context['logs_info'] = Logger.objects.filter(user=user,logtype='I').order_by('-created')
	context['logs_access'] = Logger.objects.filter(user=user,logtype='A').order_by('-created')
	context['logs_error'] = Logger.objects.filter(user=user,logtype='E').order_by('-created')

	return render(request, 'accounts/logs_list.html', context)

def accounts_role(request):
	data = {}

	pk = request.GET.get('role')
	group = get_object_or_404(Role, pk=pk)

	data['is_group'] = group.is_group

	return JsonResponse(data)

def accounts_permissions_list(request):

	instance = get_object_or_404(User.objects.prefetch_related('user_permisssion'), pk=request.GET.get('pk'))
	#-- List of menu modules
	menu_list = User.modules_list()

	menu_modules = []
	submenu_modules = []
	options_list = []

	for item_user in instance.user_permisssion.all().select_related('menu_item','menu_subitems'):
		if item_user.menu_item.is_menu == True:
			if item_user.menu_item.has_submenu == False:
				menu_modules.append(str(item_user.menu_item.pk)+'|0')
				options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item_user.menu_item.title,'value':str(item_user.menu_item.pk)+'|0','selected':True}))

		if item_user.menu_subitems is not None:
			if item_user.menu_subitems.is_submenu == True:
				submenu_modules.append(str(item_user.menu_subitems.pk)+'|1')
				options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item_user.menu_item.title+' - '+item_user.menu_subitems.title,'value':str(item_user.menu_subitems.pk)+'|1','selected':True}))

	if request.user.is_superuser:
		for item in menu_list:
			if item.has_submenu == False:
				if str(item.pk)+'|0' not in menu_modules:
					options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item.title,'value':str(item.pk)+'|0','selected':False}))

			for subitem in item.subitems.all():
				if str(subitem.pk)+'|1' not in submenu_modules:
					options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item.title+' - '+subitem.title,'value':str(subitem.pk)+'|1','selected':False}))

	elif instance != request.user and not request.user.is_superuser:
		for item in request.user.user_permisssion.all():
			if item.menu_item.has_submenu == False:
				if str(item.menu_item.pk)+'|0' not in menu_modules:
					options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item.menu_item.title,'value':str(item.menu_item.pk)+'|0','selected':False}))
			else:
				if str(item.menu_subitems.pk)+'|1' not in submenu_modules:
					options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item.menu_item.title+' - '+item.menu_subitems.title,'value':str(item.menu_subitems.pk)+'|1','selected':False}))

	elif instance == request.user:
		for item in request.user.user_permisssion.all():
			if item.menu_item.has_submenu == False:
				if str(item.menu_item.pk)+'|0' not in menu_modules:
					options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item.menu_item.title,'value':str(item.menu_item.pk)+'|0','selected':False}))
			else:
				if str(item.menu_subitems.pk)+'|1' not in submenu_modules:
					options_list.append(render_to_string('core/snippets/dropdown_list_options.html',{'title':item.menu_item.title+' - '+item.menu_subitems.title,'value':str(item.menu_subitems.pk)+'|1','selected':False}))

	return JsonResponse(options_list,safe=False)


def resend_mail(request, customer_pk):
	data = {}
	context = {}
	user = get_object_or_404(User, customer__pk=customer_pk, is_client=True)
	if request.is_ajax() and request.method == 'POST':
		password = get_random_string(10)
		user.set_password(password)
		user.save()
		User.activation_email(request,user,password)
		data['form_is_valid'] = True
	else:
	#-- Parameters modal form
		context['url_post'] = '/panel/accounts/resend_mail/%s/' %(customer_pk)
		data['form_is_valid'] = False
		data['html_sendmail_shop'] = render_to_string('core/snippets/modal_sendmail.html', context, request=request)
	return JsonResponse(data)
		