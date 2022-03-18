# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from dateutil.relativedelta import relativedelta

import json
import stripe
import logging
import locale

from decouple import config

from panel.core.decorators import access_for_user
from panel.core.utils import user_logs, sendmail
from panel.core.context_processors import menu_user
from panel.accounts.models import User
from panel.authorization.forms import LoginForm, RecoverStoreForm
from portal.shop.models import ShopOrder


logger = logging.getLogger(__name__)

#locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')
# Create your views here.

def login_account(request):
	context = {}
	if request.user.is_authenticated:
		return redirect('authorization:dashboard')
	else:
		if request.method == 'POST':
			user = authenticate(request,email=request.POST.get('email',None), \
										password=request.POST.get('password',None), \
									)
			if user:
				context['form'] = LoginForm(request.POST,user=user)
				if context['form'].is_valid():
					login(request, user)

					#-- User Logs (Info, Access, Error)
					user_logs(request,None,'A','Acceso al sistema')
					return redirect('authorization:dashboard')
			else:
				context['error'] = 'Tus credenciales no coinciden, favor de verificarlas'
				context['form'] = LoginForm(user=None)

		else:
			context['form'] = LoginForm(user=None)

	return render(request, 'authorization/login.html', context)

@access_for_user
def dashboard(request):
	context = {}
	context['total_shoppings_stores'] = ShopOrder.total_shoppings_stores(request)
	context['total_shipping_stores'] = ShopOrder.total_shipping_stores(request)
	context['total_earnings_stores'] = ShopOrder.total_earnings_stores(request)
	context['total_products_stores'] = ShopOrder.total_products_stores(request)

	#-- Totals
	return render(request, 'authorization/dashboard.html', context)

def logout_account(request):

	#-- User Logs (Info, Access, Error)
	user_logs(request,None,'A','Cierre de Sesión')

	logout(request)
	return redirect('authorization:login')


def recover_store(request):
	context = {}
	if request.method == 'POST':
		context['form'] = RecoverStoreForm(request.POST)
		if context['form'].is_valid():
			user = User.objects.get(email__iexact=context['form'].cleaned_data['email'])
			subject = '4Shop :: Recuperación de tienda'
			message = render_to_string('authorization/includes/recover_store_email.html', {
										'store' : Store.objects.get(customer__users=user),
										'email' : context['form'].cleaned_data['email'],
										})
			sendmail(subject, message, settings.DEFAULT_FROM_EMAIL, user.email)
			return render(request, 'authorization/recover_store_complete.html', context)
	else:
		context['form'] = RecoverStoreForm()
	return render(request, 'authorization/recover_store_form.html', context)



