# -*- coding: utf-8 -*-
from django import forms
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist

from panel.accounts.models import User
from .models import Address

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label = 'Email',
        error_messages = {'required': 'Debe capturar el Email'},
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'readonly': 'readonly',
            }
        )
    )
    first_name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required': 'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    last_name = forms.CharField(
        label = 'Apellidos',
        error_messages = {'required': 'Debe capturar los apellidos'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    phone = forms.CharField(
        label = 'Teléfono',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    avatar = forms.ImageField(
        label = 'Foto',
        required = False,
        widget = forms.FileInput(

        )
    )
    birthday = forms.CharField(
        label = 'Fecha de nacimiento',
        error_messages = {'required':'Debe de capturar su fecha de nacimiento'},
        widget = forms.TextInput(
            attrs = {
                'placeholder' : 'Fecha de nacimiento',
                'type':'date',
                'class' : 'form-control w-100 inputLogin',
            }
        )
    )
    gender = forms.ChoiceField(
        label = 'Peso',
        choices = User.GENDER,
        widget = forms.Select(
            attrs = {
                'class': 'select2'
            }
        )
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'
            if self.fields[field].required:
                self.fields[field].label = format_html('{} <span class="text-danger">*</span>',self.fields[field].label)

    def clean_email(self):
        cd = self.cleaned_data
        if not self.instance.pk:
            email = User.objects.filter(email__iexact=cd['email']).exclude(pk=self.user.id).exists()

            if email:
                raise forms.ValidationError('Este correo ya está registrado')

        return cd['email']

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name','phone','avatar', 'birthday', 'gender',)

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label = 'Contraseña actual',
        error_messages = {'required' : 'Debe capturar la contraseña actual'},
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label = 'Nueva contraseña',
        error_messages = {'required' : 'Debe capturar la nueva contraseña'},
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label = 'Confirmar contraseña',
        error_messages = {'required' : 'Debe confirmar la nueva contraseña'},
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control input-sm'
            if self.fields[field].required:
                self.fields[field].label = format_html('{} <span class="text-danger">*</span>',self.fields[field].label)

    def clean_current_password(self):
        cd = self.cleaned_data

        password = self.user.check_password(cd['current_password'])

        if not password:
            raise forms.ValidationError('La contraseña actual no coincide')

        return cd['current_password']

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd['password']
        password2 = cd['password2']

        if password != password2:
            raise forms.ValidationError('Las contraseña nueva y la confirmación no coinciden.')

        return password2

    class Meta:
        fields = ('currentpassword', 'password', 'password2')

class AddressForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required':'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Nombre'
            }
        )
    )
    address = forms.CharField(
        label = 'Direccion',
        error_messages = {'required':'Debe capturar la dirección'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Dirección'
            }
        )
    )
    zip_code = forms.CharField(
        label = 'CP',
        error_messages = {'required':'Debe capturar el código postal'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'CP',
                'autocomplete': 'xyz1231'
            }
        )
    )
    num_ext = forms.CharField(
        label = 'N° Exterior',
        error_messages = {'required':'Capture un número','invalid':'Introduzca un valor en digitos','max_digits':'Favor de introducir un valor menor a 5 digitos'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'N° exterior'
            }
        )
    )
    num_int = forms.CharField(
        label = 'N° Interior',
        required = False,
        error_messages = {'required':'Capture un número','invalid':'Introduzca un valor en digitos','max_digits':'Favor de introducir un valor menor a 5 digitos'},
        help_text= 'Opcional',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'N° interior'
            }
        )
    )
    city = forms.CharField(
        label = 'Ciudad',
        error_messages = {'required':'Debe capturar la ciudad'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Ciudad',
                'autocomplete': 'xyz1231'
            }
        )
    )
    state = forms.CharField(
        label = 'Estado',
        error_messages = {'required':'Debe capturar el estado'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Estado',
                'autocomplete': 'xyz1231'

            }
        )
    )
    suburb = forms.CharField(
        label = 'Colonia',
        error_messages = {'required':'Debe capturar la colonia'},
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Colonia',
            }
        )
    )
    default = forms.BooleanField(
        label = 'Predeterminada',
        required = False,
        initial = True,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'js-switch'
            }
        )
    )
    class Meta:
        model = Address
        fields = ('name', 'address', 'zip_code', 'num_ext', 'city', 'state', 'suburb', 'default')

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label = format_html('{} <span class="text-danger">*</span>',self.fields[field].label)
    def clean(self):
        cd = self.cleaned_data
        try:
            inst =  Address.objects.get(pk=self.instance.pk)
            obj = Address.objects.filter(user=self.request.user, default=True).exclude(pk=self.instance.pk).exists()
            if not inst.default:
                if not obj:
                    self.add_error('default', 'Una dirección debe de ser predeterminada')
        except ObjectDoesNotExist:
            pass
        return cd