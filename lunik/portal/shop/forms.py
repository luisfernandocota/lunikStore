# -*- coding: utf-8 -*-
from django import forms

from django.utils.html import format_html
from django.forms import ModelChoiceField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from portal.shop.models import ShopOrder,ShopOrderDelivery, Contact, ShopOrderCancel
from panel.products.models import Product
SHIPPING_OPTIONS = (
    #('SS','Pick up at school'),
    ('HS','Enviar a domicilio'),
)

class ShopOrderForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required':'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Nombre(s)'
            }
        )
    )
    email = forms.EmailField(
        label = 'Email',
        error_messages = {'required':'Debe capturar el correo'},
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'email@mail.com',
            }
        )
    )
    phone = forms.CharField(
        label = 'Teléfono',
        error_messages = {'required':'Debe capturar el teléfono'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '(999) 999 9999'
            }
        )
    )

    class Meta:
        model = ShopOrder
        fields = ('name','email','phone')




class ShopOrderDeliveryForm(forms.ModelForm):
    address = forms.CharField(
        label = 'Dirección',
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
                'placeholder' : 'CP'
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
        error_messages = {'required':'Capture la ciudad'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Ciudad',
                'readonly': 'readonly'
            }
        )
    )
    state = forms.CharField(
        label = 'Estado',
        error_messages = {'required':'Capture el estado'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Estado',
                'readonly': 'readonly'
            }
        )
    )
    suburb = forms.CharField(
        label = 'Colonia',
        error_messages = {'required':'Capture la colonia'},
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'placeholder' : 'Colonia',
                'onload': 'get_zipcode()'
            }
        )
    )
    # has_delivery = forms.ChoiceField(
    #     label = 'Enviar a',
    #     required = False,
    #     choices = SHIPPING_OPTIONS,
    #     widget = forms.Select(
    #         attrs = {
    #             'class':'custom-select my-1 mr-sm-2 custom-select-fd',
    #             'data-shipping': "0",
    #             'data-shipping-limit': "0",
    #         }
    #     )
    # )

    class Meta:
        model = ShopOrderDelivery
        fields = ('address','zip_code','city','state', 'suburb', 'num_ext', 'num_int')


class ProductShopCart(forms.Form):
    quantity = forms.IntegerField(
        label = 'Quantity',
        help_text = 'Personalized items must be entered individually',
        error_messages = {
                    'required':'Debe capturar la cantidad','invalid':'La cantidad debe de ser solo en dígitos',
                    'min_value':'Debe captura mínimo 1','max_value':'Ls cantidad debe ser menor a 99'
        },
        initial = 1,
        validators = [MinValueValidator(1),MaxValueValidator(99)],
        widget = forms.TextInput(
            attrs = {
                'class':'form-control text-center',
                'name':'num-product'
            }
        )
    )
    sizes = forms.ModelChoiceField(
        label = 'Tipo',
        empty_label = 'Elija ...',
        to_field_name = 'name',
        queryset = Product.objects.none(),
        widget = forms.Select(
            attrs = {
                'class':'form-select',
            }
        )
    )
    product_pk = forms.CharField(
        label = 'Product PK',
        widget = forms.HiddenInput()
    )
    name_personalization = forms.CharField(
        label = 'Nombre personalizado',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )
    number = forms.IntegerField(
        label = 'Number',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'style': 'width:150px'

            }
        )
    )

    def __init__(self, *args, **kwargs):
        sizes = kwargs.pop('product_sizes')
        self.product_pk = kwargs.pop('product_pk')
        super(ProductShopCart, self).__init__(*args, **kwargs)
        product = Product.objects.get(pk=self.product_pk)
        if product.products_properties.has_personalization:
            self.fields['quantity'].widget = forms.HiddenInput()
        self.fields['sizes'].queryset = sizes
        self.fields['sizes'].label_from_instance = lambda obj: "%s + $(%s)  " % (obj.name, obj.charge) if obj.charge else obj.name

    def clean(self):
        product = Product.objects.get(pk=self.product_pk)
        cd = self.cleaned_data
        if not cd.get('name_personalization') and product.products_properties.has_personalization:
            self._errors['name_personalization'] = self.error_class(['Captura el nombre personalizado'])
        return cd

class QuantityCartForm(forms.Form):
    quantity = forms.IntegerField(
        label = 'Cantidad',
        error_messages = {
                    'required':'Debe capturar la cantidad','invalid':'La cantidad debe de ser solo en dígitos',
                    'min_value':'Debe captura mínimo 1','max_value':'Ls csntidad debe ser menor a 99'
        },
        initial = 1,
        validators = [MinValueValidator(1),MaxValueValidator(99)],
        widget = forms.TextInput(
            attrs = {
                'class':'form-control',
                'style':'width:30%'
            }
        )
    )

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required':'Debe capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class': 'sizefull s-text7 p-l-22 p-r-22',
                'placeholder' : 'Nombre(s)'
            }
        )
    )
    email = forms.EmailField(
        label = 'Email',
        error_messages = {'required':'Debe capturar el correo'},
        widget = forms.EmailInput(
            attrs = {
                'class': 'sizefull s-text7 p-l-22 p-r-22',
                'placeholder' : 'Correo electrónico',
            }
        )
    )
    phone = forms.CharField(
        label = 'Teléfono',
        error_messages = {'required':'Debe capturar el teléfono'},
        widget = forms.TextInput(
            attrs = {
                'class': 'sizefull s-text7 p-l-22 p-r-22',
                'placeholder' : 'Teléfono'
            }
        )
    )
    comment = forms.CharField(
        label = 'Comentarios',
        error_messages = {'required':'Debe capturar el nombre'},
        widget = forms.Textarea(
            attrs = {
                'class': 'dis-block s-text7 size20 bo4 p-l-22 p-r-22 p-t-13 m-b-20',
                'rows': '5',
                'placeholder' : 'Comentarios',
            }
        )
    )
    class Meta:
        model = Contact
        fields = ('name','email','phone', 'comment')


    def __init__(self,*args,**kwargs):
        super(ContactForm,self).__init__(*args,**kwargs)

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label = format_html('{} <span class="text-danger">*</span>',self.fields[field].label)

class OrderCanceledForm(forms.ModelForm):
    comment = forms.CharField(
        label = 'Comentarios',
        error_messages = {'required':'Debe capturar algún comentario'},
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows': '5',
                'placeholder' : 'Dinos que estuvo mal en tu pedido',
            }
        )
    )
    class Meta:
        model = ShopOrderCancel
        fields = ('comment',)