# -*- coding: utf-8 -*-
from django import forms

from .models import OrderDelivery
class OrderDeliveryForm(forms.ModelForm):
    delivery_company = forms.CharField(
        label = 'Comañia de envios',
        error_messages = {'required':'Debe de capturar la compañia'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
            }
        )
    )
    tracking_number = forms.CharField(
        label = 'Número de rastreo',
        error_messages = {'required':'Debe de capturar el numero de rastero'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
            }
        )
    )
    range_date_start = forms.DateField(
        label = 'Fecha inicial',
        error_messages = {'required':'Debe de capturar una fecha inicial'},
        widget = forms.TextInput(
            attrs = {'class' : 'form-control-sm form-control'},
        )
    )
    range_date_end = forms.DateField(
        label = 'Fecha final',
        error_messages = {'required':'Debe de capturar una fecha final'},
        widget = forms.TextInput(
            attrs = {'class' : 'form-control-sm form-control'},
        )
    )
    class Meta:
        model = OrderDelivery
        fields = ('delivery_company','tracking_number', 'range_date_start', 'range_date_end')


class SearchStoreForm(forms.Form):
    query = forms.CharField(
        label = 'Buscar',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'input-sm form-control',
                'placeholder': 'Buscar'
            }
        )
    )
class SearchOrderForm(forms.Form):
    query = forms.CharField(
        label = 'Buscar',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'input-sm form-control',
                'placeholder': 'Buscar orden'
            }
        )
    )
