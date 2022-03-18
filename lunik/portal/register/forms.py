# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from panel.accounts.models import User

def UniqueEmailValidator(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('Este correo ya ha sido registrado.')

class RegisterForm(forms.ModelForm):
	email = forms.EmailField(
		label = 'Email',
		error_messages = {'required': 'Debe de capturar su Email'},
		widget = forms.EmailInput(
			attrs = {
				'placeholder' : 'Correo electrónico',
				'class' : 'form-control form-control-sm'
			}
		)
	)
	password = forms.CharField(
		label = 'Contraseña',
		error_messages = {'required' : 'Debe capturar la contraseña'},
		widget = forms.PasswordInput(
			attrs = {
				'placeholder' : 'Contraseña',
				'class' : 'form-control form-control-sm',
			}
		)
	)
	first_name = forms.CharField(
		label = 'Nombre(s)',
		error_messages = {'required': 'Debe de capturar su Nombre(s)'},
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Nombre(s)',
				'class' : 'form-control form-control-sm',
			}
		)
	)
	last_name = forms.CharField(
		label = 'Apellidos',
		error_messages = {'required': 'Debe de capturar sus Apellidos'},
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Apellidos',
				'class' : 'form-control form-control-sm',
			}
		)
	)
	birthday = forms.DateField(
		label = 'Fecha de nacimiento',
		error_messages = {'required': 'Debe de capturar su fecha de nacimiento'},
		widget = forms.DateInput(
			attrs = {
				'class' : 'form-control form-control-sm',
			}
		)
	)
	gender = forms.CharField(
		label = 'Género',
		widget = forms.RadioSelect(
			choices = User.GENDER,
			attrs = {
				'class':'form-check-input',
			}
		)
	)
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		self.customer = kwargs.pop('customer')
		super(RegisterForm, self).__init__(*args, **kwargs)
	def clean_email(self):
		cd = self.cleaned_data
		email = User.objects.filter(email__iexact=cd['email'], is_customer=True, customer=self.customer).exclude(pk=self.user.id).exists()
		if email:
			raise forms.ValidationError('Este correo ya ha sido registrado')

		return cd['email']
	class Meta:
		model = User
		fields = ('email','first_name','last_name', 'password', 'birthday', 'gender')
