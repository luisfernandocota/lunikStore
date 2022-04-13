# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from django.template.loader import render_to_string
from django.db.models import Q, CharField,DateField, DecimalField, Case, Value, When, Sum, F
from django.shortcuts import get_object_or_404

from panel.core.utils import sendmail

from panel.accounts.models import User
from panel.products.models import Product, Coupon


PENDIENTE = 'PE'
PROCESO = 'EP'
ENVIADO = 'EE'
ENTREGADO = 'EN'

SHIPPING_STATUS = (
    (PENDIENTE, 'Pendiente'),
    (PROCESO, 'En proceso'),
    (ENVIADO, 'Enviado'),
    (ENTREGADO, 'Entregado')
)

def folio_order():
    date_year = str(timezone.now().today().date()).split("-")
    year = date_year[0][2:4]

    fill = ShopOrder.objects.filter(created__startswith=timezone.now().today().date()).count()

    if fill:
        fill = fill + 1
        return "%s%s%s-%s" % (year,date_year[1],date_year[2],fill)
    else:
        return "%s%s%s-%s" % (year,date_year[1],date_year[2],1)

class State(models.Model):
    name = models.CharField(max_length=100, verbose_name='Estado')

    class Meta:
        db_table = 'states'

    def __str__(self):
        return self.name

# Create your models here.
class ShopOrder(TimeStampedModel):
    folio = models.CharField(max_length=30,default=folio_order,verbose_name='Order Folio')
    name = models.CharField(max_length=120,verbose_name='Name')
    email = models.EmailField(max_length=80,verbose_name='Email')
    phone = models.CharField(max_length=30,verbose_name='Phone')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shop_orders', verbose_name='Customer', on_delete=models.CASCADE, null=True)
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'shop_orders'
        verbose_name = 'Shop order'

    def __str__(self):
        return self.name

    @staticmethod
    def total_shoppings_stores(request):
        shop = ShopOrder.objects.select_related('order_payment')\
                                .filter(status=True)\
                                .aggregate(total=models.Sum('order_payment__total'))

        if not shop.get('total'):
            return 0

        return shop.get('total',0)

    @staticmethod
    def total_shipping_stores(request):
        shop = ShopOrder.objects.select_related('order_payment')\
                                .filter(status=True)\
                                .aggregate(total=Sum('order_payment__shipping'))

        if not shop.get('total'):
            return 0

        return shop.get('total',0)

    @staticmethod
    def total_earnings_stores(request):
        shop = ShopOrder.objects.select_related('order_payment')\
                                .filter(status=True)\
                                .aggregate(total=(Sum('order_payment__total')+Sum('order_payment__shipping')))

        if not shop.get('total'):
            return 0

        return shop.get('total',0)

    @staticmethod
    def total_products_stores(request):
        shop = ShopOrder.objects.prefetch_related('products_orders')\
                                .filter(status=True)\
                                .aggregate(total=Sum('products_orders__quantity'))

        if not shop.get('total'):
            return 0

        return shop.get('total',0)

    @staticmethod
    def current_shopping(request):
        current_shopping = ShopOrder.objects\
                                            .filter(status=True).order_by('-created')[:5]

        return current_shopping

    @staticmethod
    def sendmail_order(request, order, info):
        context = {}
        user = get_object_or_404(User, is_client=True)
        context['order'] = order
        context['request'] = request
        context['info'] = info
        if info.same_email:
            mail_list = [info.email_store, user.email]

        else:
            mail_list = [order.store.store_meta.info.email_store]

            #-- Sendmail to Client 4shop
        message2 = render_to_string('shop/includes/order_review_email.html',context)
        sendmail('%s :: Compra de productos' % (order.store.name), message2, settings.DEFAULT_FROM_EMAIL, mail_list)
        #-- Sendmail order to customer (From,to)
        message = render_to_string('shop/includes/order_payment_email.html',context)
        sendmail('%s :: Compra de productos' % (order.store.name), message, settings.DEFAULT_FROM_EMAIL,order.email)

        return True

    def total_products(self):
        return sum(item.quantity for item in self.products_orders.all())

    def total_shopping(self):
        return (self.order_payment.total + self.order_payment.shipping)
    def subtotal_shopping(self):
        return (self.order_payment.total)

class ShopOrderCancel(TimeStampedModel):
    order = models.OneToOneField(ShopOrder,related_name='order_cancel',verbose_name='Shop order', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comment')

    class Meta:
        db_table = 'shop_orders_canceled'

    def __str__(self):
        return self.order.folio


# Create your models here.
class ShopOrderDelivery(models.Model):
    order = models.OneToOneField(ShopOrder,related_name='order_delivery',verbose_name='Shop order', on_delete=models.CASCADE)
    address = models.CharField(max_length=120,verbose_name='Address')
    zip_code = models.CharField(max_length=5,verbose_name='Zip code')
    num_ext = models.CharField(max_length=5, verbose_name='Num Ext')
    num_int = models.CharField(max_length=5, verbose_name='Num Int')
    city = models.CharField(max_length=80,verbose_name='City')
    state = models.CharField(max_length=30,verbose_name='State')
    suburb = models.CharField(max_length=50, verbose_name='Suburb')
    #state = models.ForeignKey(State,related_name='+',verbose_name='State')
    country = models.CharField(max_length=80,verbose_name='Country',default='MX')

    class Meta:
        db_table = 'shop_orders_delivery'
        verbose_name = 'Order delivery'

    def __str__(self):
        return self.order

class ShopOrderProduct(models.Model):
    order = models.ForeignKey(ShopOrder,related_name='products_orders',verbose_name='Shop order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='products_orders',verbose_name='Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Price')
    quantity = models.PositiveSmallIntegerField(verbose_name='Quantity')
    name_personalization = models.CharField(max_length=120, verbose_name='Name Personalization', null=True)
    size = models.CharField(max_length=50,verbose_name='Size')
    name = models.CharField(max_length=250,verbose_name='Name',blank=True)
    number = models.PositiveSmallIntegerField(verbose_name='Number',blank=True,null=True)

    class Meta:
        db_table = 'shop_orders_products'
        verbose_name = 'Order Product'

    def __str__(self):
        return self.product

    @staticmethod
    def products_save(cart,order):

        products_list = []

        for item in cart:
            variants_keys = item['variants'].keys()

            for key in variants_keys:
                #-- Save products
                products_list.append(
                    ShopOrderProduct(
                        order=order,
                        product=item['product'],
                        #price=item['price'],
                        price=Decimal(item['price']) + Decimal(item['variants'][key].get('charge_custom',0.00)) +
                                            Decimal(item['variants'][key].get('charge_size',0.00)),
                        quantity=item['variants'][key]['quantity'],
                        #quantity=item['variants'][key],
                        size=item['sizes'][key],
                        name_personalization=item['variants'][key].get('name_personalization',''),
                        name=item['variants'][key].get('name',''),
                        number=item['variants'][key].get('number'),
                    )
                )

        return products_list

    def total_products_price(self):
        return self.price * self.quantity

class ShopOrderPayment(models.Model):
    order = models.OneToOneField(ShopOrder,related_name='order_payment',verbose_name='Shop order', on_delete=models.CASCADE)
    payment_intent = models.CharField(max_length=100,verbose_name='Payment Intent ID')
    client_secret = models.CharField(max_length=120,verbose_name='Client secret ID')
    total = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Total')
    shipping = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Shipping',blank=True)
    date_payment = models.DateField(verbose_name='Payment date',auto_now_add=True)
    coupon = models.ForeignKey(Coupon, related_name='order_payment', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=SHIPPING_STATUS , default='PE')

    class Meta:
        db_table = 'shop_orders_payments'
        verbose_name = 'Order Payment'

    def __str__(self):
        return self.stripe_folio

class Contact(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    phone = models.CharField(max_length=30, verbose_name='Teléfono')
    email = models.EmailField(max_length=200, verbose_name='Correo electrónico')
    comment = models.TextField(verbose_name='Comentario')

    class Meta:
        db_table = 'contact'
        ordering = ('-created',)
        verbose_name = 'Contacto'
