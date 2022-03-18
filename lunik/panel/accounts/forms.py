# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Case

from panel.config.models import ModuleItem
from .models import User, Role, UserModuleGroup

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        label = 'Email',
        error_messages = {'required': 'Debe capturar el Email'},
        widget = forms.EmailInput(
            attrs = {
                'class' : 'form-control required',
                'aria-required' : 'True',
                'placeholder' : 'Correo electrónico'
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
        queryset = Role.objects.filter(status=True).exclude(name__iexact='Superadmin').exclude(name__iexact='Reseller Director').exclude(name__iexact='Reseller Ejecutivo').order_by('name'),
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
                'class':'form-check-input form-check-success'
            }
        )
    )
    is_superadmin = forms.BooleanField(
        label = 'Superadmin',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input form-check-success'
            }
        )
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass
        #cd = super(UserForm,self).clean()
        #if not self.user.user_groups.exists():
        #	if cd.get('user_type') is None:
        #		self.add_error('user_type','Debe seleccionar el rol de usuario')

        #return cd

    def clean_email(self):
        cd = self.cleaned_data

        if self.instance.pk:
            email = User.objects.filter(email__iexact=cd['email'], is_superuser=True).exclude(pk=self.user.id).exists()
        else:
            email = User.objects.filter(email__iexact=cd['email'], is_superuser=True).exists()

        if email:
            raise forms.ValidationError('Este correo ya está registrado')

        return cd['email']

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name', 'role','is_active','is_superadmin')

class RoleForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required':'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    description = forms.CharField(
        label = 'Descripción',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    is_group = forms.BooleanField(
        label = 'Es grupo',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'js-switch',
            }
        )
    )

    class Meta:
        model = Role
        fields = ('name','description','is_group')

class UserModuleGroupForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        label = 'Rol de Usuario',
        queryset =  Role.objects.none(),
        empty_label = 'Seleccione...',
        error_messages = {'required':'Debe capturar el rol de usuario'},
        widget = forms.Select(
            attrs = {
                'class': 'form-control select2'
            }
        )
    )

    class Meta:
        model = UserModuleGroup
        fields = ('role',)

    def __init__(self,*args,**kwargs):
        super(UserModuleGroupForm,self).__init__(*args,**kwargs)

        groups_pk = list(UserModuleGroup.objects.values_list('role__pk',flat=True).filter(status=True))
        if self.instance.pk:
            self.fields['role'].queryset = Role.objects.filter(status=True,is_group=True,pk__in=groups_pk)
        else:
            self.fields['role'].queryset = Role.objects.filter(status=True,is_group=True).exclude(pk__in=groups_pk)
