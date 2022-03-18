# -*- coding: utf-8 -*-
from django import forms
from django_summernote.widgets import SummernoteWidget

from panel.config.models import PanelAdmin, ModuleItem, ModuleSubItem, TemplateComponent

class PanelAdminForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Título',
        error_messages = {'required':'Debe capturar el titulo'},
        widget = forms.TextInput()
    )
    url = forms.URLField(
        label = 'URL',
        required = False,
        widget = forms.TextInput()
    )
    author = forms.CharField(
        label = 'Autor',
        required = False,
        widget = forms.TextInput()
    )
    logo = forms.ImageField(
        label = 'Logo',
        error_messages = {'required':'Debe capturar el logo'},
        widget = forms.FileInput()
    )

    class Meta:
        model = PanelAdmin
        fields = ('title','url','author','logo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ModuleItemForm(forms.ModelForm):
    app_label = forms.CharField(
        label = 'App Label',
        error_messages = {'required':'Debe capturar el label'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    title = forms.CharField(
        label = 'Título',
        error_messages = {'required':'Debe capturar el título'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    module = forms.CharField(
        label = 'Módulo',
        required = False,
        error_messages = {'required':'Debe capturar el nombre del módulo'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control '
            }
        )
    )
    url = forms.CharField(
        label = 'URL',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control '
            }
        )
    )
    icon = forms.CharField(
        label = 'Icono',
        error_messages = {'required':'Debe capturar la clase del ícono'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control '
            }
        )
    )
    order = forms.CharField(
        label = 'Orden',
        error_messages = {'required':'Debe capturar el orden'},
        initial = 0,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )
    has_submenu = forms.BooleanField(
        label = 'Con Submenu',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input form-check-success'
            }
        )
    )
    is_module = forms.BooleanField(
        label = 'Es Módulo',
        required = False,
        initial = True,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input form-check-success'
            }
        )
    )
    is_store = forms.BooleanField(
        label = 'Solo tienda',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input form-check-success'
            }
        )
    )

    class Meta:
        model = ModuleItem
        fields = ('app_label','title','module','url','icon','order','has_submenu','is_module','is_store')

class ModuleSubItemForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        label = 'Menú',
        queryset = ModuleItem.objects.filter(status=True,has_submenu=True),
        empty_label = 'Seleccione menú',
        error_messages = {'required':'Debe seleccionar el menú'},
        widget = forms.Select(
            attrs = {
                'class': 'form-control select2'
            }
        )
    )
    title = forms.CharField(
        label = 'Título',
        error_messages = {'required':'Debe capturar el título'},
        widget = forms.TextInput()
    )
    module = forms.CharField(
        label = 'Módulo',
        error_messages = {'required':'Debe capturar el nombre del módulo'},
        widget = forms.TextInput()
    )
    url = forms.CharField(
        label = 'URL',
        required = False,
        widget = forms.TextInput()
    )
    icon = forms.CharField(
        label = 'Icono',
        required = False,
        widget = forms.TextInput()
    )
    order = forms.CharField(
        label = 'Orden',
        error_messages = {'required':'Debe capturar el orden'},
        initial = 0,
        widget = forms.TextInput()
    )
    is_store = forms.BooleanField(
        label = 'Solo tienda',
        required = False,
        initial = True,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input form-check-success'
            }
        )
    )

    class Meta:
        model = ModuleSubItem
        fields = ('item','title','module','url','icon','order','is_store')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields:
            if field != 'is_store':
                self.fields[field].widget.attrs['class'] = 'form-control'

class TemplateComponentForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required':'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    code = forms.CharField(
        label = 'Código',
        required = False,
        widget = forms.Textarea()
    )
    status = forms.BooleanField(
        label = '¿Activo?',
        required = False,
        initial = True,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'js-switch2'
            }
        )
    )

    class Meta:
        model = TemplateComponent
        fields = ('status','name','code')
