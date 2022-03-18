# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import locale
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from django.template.loader import render_to_string
from django.contrib import messages

from panel.core.utils import user_logs, sendmail
from portal.shop.models import ShopOrder
# Create your models here.

class OrderDelivery(TimeStampedModel):

    order = models.OneToOneField(ShopOrder,related_name='shop_order_delivery',verbose_name='Shop order', on_delete=models.CASCADE)
    delivery_company = models.CharField(max_length=130, verbose_name='Delivery Company', blank=True)
    range_date_start = models.DateField(verbose_name='Date inital', null=True)
    range_date_end = models.DateField(verbose_name='Date end', null=True)
    tracking_number = models.CharField(max_length=100, verbose_name='Tracking number', blank=True)

    class Meta:
        db_table = 'order_delivery'

    @staticmethod
    def sendmail_order(request, order):

        context = {}

        context['order'] = order
        context['request'] = request

        #-- Sendmail order to customer (From,to)
        message = render_to_string('orders/includes/delivery_mail.html',context)
        sendmail('Lunik Diseño :: Detalle de envio', message, settings.DEFAULT_FROM_EMAIL,order.email)

        return True

    def fields_fill(self):
        if self.delivery_company == '' and self.tracking_number == '':
            return False
        else:
            return True

    @staticmethod
    def sendmail_shop_link(request,instance,url,namespace):

        context = {}
        data = {}

        if request.is_ajax() and request.method == 'POST':

            context['order'] = instance
            message = render_to_string('orders/includes/orders_sendmail.html',context,request=request)
            sendmail('Lunik Diseño :: Compra de productos', message, settings.DEFAULT_FROM_EMAIL,instance.email)

            messages.success(request, 'Reenvio de correo enviado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Reenvio de correo enviado satisfactoriamente')

            data['form_is_valid'] = True
            data['url_redirect'] = url

        else:
            #-- Parameters modal form
            context['obj_campaign'] = instance
            context['url_post'] = namespace

            data['html_sendmail_shop'] = render_to_string('orders/includes/orders_sendmail_modal.html', context, request=request)

        return data

    def get_day_start(self):
        return self.range_date_start.strftime('%d')
    def get_day_end(self):
        return self.range_date_end.strftime('%d')
    def get_month(self):
        return self.range_date_end.strftime('%B')