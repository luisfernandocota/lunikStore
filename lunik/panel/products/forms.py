from dataclasses import fields
from re import A

from datetime import date

from django import forms
from django.utils.html import format_html
from django_summernote.widgets import SummernoteWidget


from .models import CouponProduct, Coupon, Product, ProductHexaCode, ProductProperty, ProductSize

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Producto',
        error_messages = {'required':'Debe capturar el nombre del producto'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. Playera',
            }
        )
    )
    price = forms.CharField(
        label = 'Precio base',
        error_messages = {'required':'Debe capturar el precio'},
        initial = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. $100',
            }
        )
    )
    brand = forms.CharField(
        label = 'Marca',
        error_messages = {'required':'Debe capturar la marca'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. Addidas',
            }
        )
    )
    model = forms.CharField(
        label = 'Modelo',
        error_messages = {'required':'Debe capturar el modelo'},
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. Sport',
            }
        )
    )
    description = forms.CharField(
        label = 'Descripción',
        error_messages = {'required':'Debe capturar la descripción'},
        widget = SummernoteWidget(
            attrs = {
                'width': '100%',
                'height': '100px',
            }
        )
    )
    aditional = forms.CharField(
        label = 'Información adicional',
        required = False,
        widget = SummernoteWidget(
            attrs = {
                'width': '100%',
                'height': '100px',
            }
        )
    )
    available = forms.BooleanField(
        label  = 'Disponible en tienda',
        required = False,
        initial = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class' : 'form-check-input form-check-primary'
            }
        )
    )
    sizes = forms.ModelMultipleChoiceField(
        label = 'Tipo',
        error_messages = {'required':'Debe de seleccionar al menos un tipo'},
        queryset = ProductSize.objects.none(),
        widget = forms.SelectMultiple(
            attrs = {
                'class' : 'choices form-select multiple-remove',
                'multiple': 'multiple'
            }
        )
    )
    hexacodes = forms.ModelMultipleChoiceField(
        label = 'Colores',
        error_messages = {'required':'Debe de seleccionar al menos un color'},
        queryset = ProductHexaCode.objects.none(),
        to_field_name = 'hexacode',
        widget = forms.SelectMultiple(
            attrs = {
                'class' : 'choices form-select multiple-remove',
                'multiple': 'multiple'
            }
        )
    )
    class Meta:
        model = Product
        fields = ('name','price','brand', 'model', 'description', 'aditional', 'sizes', 'hexacodes', 'available')


    def __init__(self,*args,**kwargs):

        super(ProductForm,self).__init__(*args,**kwargs)
        self.fields['hexacodes'].label_from_instance = lambda obj: format_html("{0} - {1}",obj.name,obj.hexacode)
        self.fields['sizes'].queryset = ProductSize.objects.filter(status=True).order_by('name').distinct()
        self.fields['hexacodes'].queryset = ProductHexaCode.objects.filter(status=True).order_by('name').distinct()

class ProductSizeForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required':'Debe de capturar la talla'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
            }
        )
    )
    charge = forms.DecimalField(
        label = 'Cargo extra',
        error_messages = {'invalid':'Debe introducir el cargo en dígitos','max_digits':'Favor de introducir un cargo válido'},
        required = False,
        initial = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = ProductSize
        fields = ('name','charge')

class ProductColorForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Nombre',
        error_messages = {'required':'Debe de capturar el nombre'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
            }
        )
    )
    hexacode = forms.CharField(
        label = 'Heaxadecimal',
        help_text = 'Ej. #000000',
        error_messages = {'required':'Debe de capturar el color hexadecimal'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
            }
        )
    )

    class Meta:
        model = ProductHexaCode
        fields = ('name','hexacode')

class ProductPropertyForm(forms.ModelForm):

    sell_price = forms.CharField(
        label = 'Precio venta',
        error_messages = {'required':'Debe capturar el precio de venta'},
        initial = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. $300',
                'step': '0.01'

            }
        )
    )
    sale_price = forms.CharField(
        label = 'Precio oferta',
        required = False,
        initial = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. $250',
                'step': '0.01'
            }
        )
    )
    is_sale = forms.BooleanField(
        label  = '¿Esta en oferta?',
        required = False,
        initial = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class' : 'form-check-input form-check-primary'
            }
        )
    )
    is_outstanding = forms.BooleanField(
        label  = '¿Es destacado?',
        required = False,
        initial = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class' : 'form-check-input form-check-primary'
            }
        )
    )
    shipping_price = forms.CharField(
        label = 'Precio envío',
        error_messages = {'required':'Debe capturar el precio de envío'},
        initial = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. $50',
                'step': '0.01'
            }
        )
    )
    shipping_free = forms.BooleanField(
        label  = '¿Envío gratis?',
        required = False,
        initial = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class' : 'form-check-input form-check-primary'
            }
        )
    )
    shipping_min = forms.CharField(
        label = 'Cantidad minima para envio gratis',
        error_messages = {'required':'Debe capturar la cantidad minima'},
        initial = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'placeholder':'Ej. 5',
                'step': '0.01'
            }
        )
    )
    has_personalization = forms.BooleanField(
        label  = '¿Es personalizable?',
        required = False,
        initial = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class' : 'form-check-input form-check-primary'
            }
        )
    )
    margin = forms.CharField(
        widget = forms.HiddenInput()
    )
    gain = forms.CharField(
        widget = forms.HiddenInput()
    )

    class Meta:
        model = ProductProperty
        fields = ('sell_price','sale_price', 'is_sale', 'is_outstanding', 'shipping_price' ,'shipping_free', 'shipping_min', 'has_personalization', 'margin', 'gain')

    def clean(self):
        cd = super().clean()
        if cd.get('is_sale'):
            if not cd.get('sale_price'):
                self.add_error('sale_price','Debe introducir un precio de oferta')
        return cd


class CouponForm(forms.ModelForm):
    code = forms.CharField(
        label = 'Código',
        help_text = 'Utilizar solo números y letras. Ej. cuponevent234',
        error_messages = {'required':'Debe capturar el código del cupón'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control'
            }
        )
    )
    discount = forms.IntegerField(
        label = 'Descuento',
        error_messages = {'required':'Debe capturar la descuento ($ o %)','invalid':'Debe capturar la cantidad en dígitos'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control'
            }
        )
    )
    discount_types = forms.ChoiceField(
        label = 'Tipo',
        choices = Coupon.DISCOUNT_TYPES,
        widget = forms.Select(
            attrs = {
                'class' : 'form-select'
            }
        )
    )
    no_uses = forms.IntegerField(
        label = 'No. de usos',
        required = False,
        min_value = 1,
        error_messages = {'invalid':'Debe capturar la cantidad en digitos','min_value':'La cantidad debe ser mínimo uno'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control'
            }
        )
    )
    min_purchase = forms.IntegerField(
        label = 'Compra minima',
        required = False,
        initial = 0,
        help_text = '0 = Sin compra  minima',
        error_messages = {'invalid':'Debe capturar la cantidad en digitos','min_value':'La cantidad debe ser mínimo uno'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control'
            }
        )
    )
    # use_types = forms.ChoiceField(
    #     label = 'Tipos de uso',
    #     choices = USE_TYPES,
    #     widget = forms.Select(
    #         attrs = {
    #             'class' : 'form-control select2'
    #         }
    #     )
    # )
    available = forms.BooleanField(
        label = 'Activo?',
        required = False,
        initial = True,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input form-check-primary'
            }
        )
    )
    apply_all = forms.BooleanField(
        label = '¿Aplica a todos los productos?',
        help_text = 'Al activarse esta opción, este cupón podrá usarse en cualquier producto',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input form-check-primary'
            }
        )
    )
    date_expiration = forms.DateField(
        label = 'Fecha expiración',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class':'input-sm form-control',
                'value': date.today()
            }
        )
    )
    class Meta:
        model = Coupon
        fields = ('code', 'discount', 'discount_types', 'no_uses', 'apply_all', 'date_expiration', 'available', 'min_purchase')

    def clean(self):
        cd = super(CouponForm,self).clean()

        if cd['discount_types'] == 'P':
            if cd.get('discount') > 100:
                self.add_error('discount','El porcentaje debe de estar entre 1 y 100%')

        return cd

    def clean_code(self):
        cd = self.cleaned_data

        if self.instance.pk:
            coupon = Coupon.objects.filter(code__exact=cd['code']).exclude(pk=self.instance.pk).exists()
        else:
            coupon = Coupon.objects.filter(code__exact=cd['code']).exists()

        if coupon:
            raise forms.ValidationError('Este código ya ha sido registrado')

        return cd['code']

class CouponProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        label = 'Producto',
        required = False,
        queryset = Product.objects.none(),
        widget = forms.Select(
            attrs = {
                'class' : 'form-select'
            }
        )
    )

    class Meta:
        model = CouponProduct
        fields = ('product',)
    def __init__(self, *args, **kwargs):
        self.products = kwargs.pop('products')
        super(CouponProductForm,self).__init__(*args,**kwargs)
        if self.products:
            self.fields['product'].queryset = Product.objects\
                                                .prefetch_related('sizes', 'products_gallery', 'products_properties')\
                                                .filter(status=True, available=True)\
                                                .exclude(pk__in=self.products.values_list('pk', flat=True))\
                                                .order_by('-created')
        else:
            self.fields['product'].queryset = Product.objects\
                                                .prefetch_related('sizes', 'products_gallery', 'products_properties')\
                                                .filter(status=True, available=True)\
                                                .order_by('-created')

class SearchProductForm(forms.Form):
    query = forms.CharField(
        label = 'Buscar producto',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'input-sm form-control',
                'placeholder': 'Buscar producto'
            }
        )
    )