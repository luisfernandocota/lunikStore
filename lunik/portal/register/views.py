# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext as _
import datetime

import requests

from panel.authorization.forms import LoginForm
from panel.core.tokens import account_activation_token
from panel.core.utils import sendmail, tenant_from_request
from panel.core.decorators import required_tenant
from panel.accounts.models import User, UserRequest
from .forms import RegisterForm
from panel.stores.models import Store
from panel.website.models import StoreMeta

@required_tenant
def register_user(request):
	from djadmin import s3_aws
	context = {}
	tenant = tenant_from_request(request)
	if tenant:
		store = get_object_or_404(Store, customer__tenant=tenant)
		meta = get_object_or_404(StoreMeta, store=store)
	if request.method == 'POST':
		context['register_form'] = RegisterForm(request.POST, user=request.user, customer=store.customer)
		if context['register_form'].is_valid():

			''' Begin reCAPTCHA validation '''
			recaptcha_response = request.POST.get('g-recaptcha-response')
			data = {
				'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response': recaptcha_response
			}
			r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
			result = r.json()
			''' End reCAPTCHA validation '''

			if result['success']:
				password = context['register_form'].cleaned_data['password']
				user = context['register_form'].save(commit=False)
				user.is_customer = True
				user.customer = store.customer
				user.set_password(password)
				user.save()

				#-- Send email
				uid = urlsafe_base64_encode(force_bytes(user.pk))
				token = account_activation_token.make_token(user)
				current_site = get_current_site(request)
				subject = '%s :: Registro de cuenta' % (store.name)
				message = render_to_string('register/register_email_customer.html', {
											'user': user,
											'request': request,
											'uid': uid,
											'token': token,
											'meta': meta,
											'AWS_S3_ENDPOINT_URL': s3_aws.AWS_S3_ENDPOINT_URL,
										})
				sendmail(subject, message, settings.DEFAULT_FROM_EMAIL, user.email)
				expires_key = datetime.datetime.today() + datetime.timedelta(2)
				#-- Save activation token
				user_activation = UserRequest.objects.create(user=user, uid=uid, token=token, expires_key=expires_key)

				#-- Message to user
				messages.success(request, _('Registro completado'))

				return redirect('register:done', user.pk)
			else:
				context['captcha_error'] = True
				messages.error(request, 'reCAPTCHA Invalido. Intenta otra vez.')

	else:

		context['register_form'] = RegisterForm(user=request.user, customer=store.customer)

	return render(request, 'register/register_signup.html', context)

@required_tenant
def register_done(request, pk):
	context = {}
	context['user'] = get_object_or_404(User, pk=pk)

	return render(request, 'register/register_done.html', context)

@required_tenant
def register_login(request):
	context = {}
	tenant = tenant_from_request(request)
	if tenant:
		store = get_object_or_404(Store, customer__tenant=tenant)
	if request.method == 'POST':
		user = authenticate(request,email=request.POST.get('email',None), \
							password=request.POST.get('password',None), \
							customer=store.customer, is_customer=True
						)
		if user and not user.is_superuser:
			context['form'] = LoginForm(request.POST,user=user)
			if context['form'].is_valid():
				login(request, user)
				return redirect('shop:shop_list')
		else:
			context['not_user'] = 'Tus credenciales no coinciden, favor de verificarlas'
			context['form'] = LoginForm(user=None)

	else:
		context['form'] = LoginForm(user=None)

	return render(request, 'register/register_login.html', context)

@required_tenant
def register_activation(request, uidb64, token):

	user_activation = User.activation_url(uidb64,token)

	if user_activation:
		return render(request, 'register/register_activation.html')
	else:
		return render(request, 'register/register_expire.html')
