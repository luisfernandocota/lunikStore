# -*- coding: utf-8
from django import forms
from django.contrib.auth import authenticate

from panel.accounts.models import User


class RecoverStoreForm(forms.Form):
	email = forms.EmailField(
		label = 'Email',
		error_messages = {'required' : 'Email incorrecto'},
		widget = forms.EmailInput(
			attrs = {
				'class' : 'form-control'
			}
		)
	)

	def clean_email(self):
		cd = self.cleaned_data
		email = User.objects.filter(email__iexact=cd['email']).exists()

		if not email:
			raise forms.ValidationError('No se ha encontrado el correo')

		return cd['email']

class LoginForm(forms.Form):
	email = forms.EmailField(
		label = 'Email',
		error_messages = {'required' : 'Email incorrecto'},
		widget = forms.EmailInput(
			attrs = {
				'class' : 'form-control'
			}
		)
	)
	password = forms.CharField(
		label = 'Contraseña',
		error_messages = {'required' : 'Contraseña incorrecta'},
		widget = forms.PasswordInput(
			attrs = {
				'class' : 'form-control'
			}
		)
	)

	def __init__(self,*args,**kwargs):
		self.user = kwargs.pop('user')

		super().__init__(*args,**kwargs)

	def clean(self):
		if self.user:
			if not self.user.is_active or not self.user.status:
				self.add_error('email','Usuario sin activar')

		super().clean()
