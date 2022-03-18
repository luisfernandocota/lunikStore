# -*- coding: utf-8 -*-
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse

from panel.core.utils import user_logs,delete_record
from panel.accounts.models import Role
from panel.accounts.forms import RoleForm

# Create your views here.
def roles_list(request):
	context = {}

	context['roles_list'] = Role.objects.filter(status=True).order_by('name')

	return render(request,'accounts/roles_list.html',context)

def roles_add(request):
	context = {}

	if request.method == 'POST':
		context['form'] = RoleForm(request.POST)

		if context['form'].is_valid():
			context['form'].save()

			#-- Message to user
			messages.success(request, 'Rol de usuario creado satisfactoriamente')

			#-- User Logs (Info, Access, Error)
			user_logs(request,None,'I','Rol de usuario creado satisfactoriamente')

			return redirect('accounts:roles_list')
	else:
		context['form'] = RoleForm()

	return render(request, 'accounts/roles_form.html', context)

def roles_edit(request,pk):
	context = {}

	context['instance'] = get_object_or_404(Role, pk=pk)

	if request.method == 'POST':
		context['form'] = RoleForm(request.POST, instance=context['instance'])

		if context['form'].is_valid():
			context['form'].save()

			#-- Message to user
			messages.success(request, 'Rol de usuario modificado satisfactoriamente')

			#-- User Logs (Info, Access, Error)
			user_logs(request,None,'I','Rol de usuario modificado satisfactoriamente')

			return redirect('accounts:roles_list')
	else:
		context['form'] = RoleForm(instance=context['instance'])

	return render(request, 'accounts/roles_form.html', context)

def roles_delete(request,pk):

	role = get_object_or_404(Role, pk=pk)

	data = delete_record(request,role,reverse('accounts:roles_list'),reverse('accounts:roles_delete',kwargs={'pk':pk}))

	if data:

		#-- Delete group permissions
		role.group.all().delete()

		#-- Delete relations users with group
		role.user.clear()

		#-- Set null all user types in user
		role.users.update(role=None)

	return JsonResponse(data)
