# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Case
from panel.accounts.models import User, Role, UserModuleGroup

class ContactForm(forms.Form):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required': 'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control not-dark'
            }
        )
    )
    email = forms.EmailField(
        label = 'Email',
        error_messages = {'required': 'Debe capturar el correo'},
        widget = forms.EmailInput(
            attrs = {
                'class' : 'form-control not-dark'
            }
        )
    )
    comment = forms.CharField(
        label = 'Comentarios',
        error_messages = {'required':'Debe de capturar los comentarios'},
        widget = forms.Textarea(
            attrs = {
                'rows': '3', 
                'class':'form-control not-dark'
            }
        )
    )
class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label = 'Email',
        error_messages = {'required': 'Debe capturar el Email'},
        widget = forms.EmailInput(
            attrs = {
                'class' : 'form-control required',
                'aria-required' : 'True',
                'placeholder' : 'Correo electrónico',
                'id' : 'id_email_2'
            }
        )
    )
    first_name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required': 'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Nombre(s)'
            }
        )
    )
    last_name = forms.CharField(
        label = 'Apellidos',
        error_messages = {'required': 'Debe capturar los apellidos'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder' : 'Apellidos'
            }
        )
    )
    role = forms.ModelChoiceField(
        label = 'Rol de Usuario',
        required = False,
        empty_label="Seleccione...",
        queryset = Role.objects.filter(status=True).order_by('name'),
        widget = forms.Select(
            attrs = {
                'class' : 'form-control select2'
            }
        )
    )
    is_active = forms.BooleanField(
        label = 'Activo',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'js-switch'
            }
        )
    )
    is_superadmin = forms.BooleanField(
        label = 'Superadmin',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'js-switch2'
            }
        )
    )

    def clean_email(self):
        cd = self.cleaned_data

        email = User.objects.filter(email__iexact=cd['email'], is_client=True).exists()
        email_super = User.objects.filter(email__iexact=cd['email'], is_superuser=True).exists()
        if email or email_super:
            raise forms.ValidationError('Este correo ya está registrado')


        return cd['email']

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name', 'role','is_active','is_superadmin')