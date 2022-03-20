# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from decimal import Decimal

from django.conf import settings
from django.db.models import Q, CharField,DateField, DecimalField, Case, Value, When, F
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone,formats
from django.contrib import messages

from panel.core.utils import pagination, sendmail

from panel.orders.forms import SearchOrderForm,SearchStoreForm, OrderDeliveryForm
from panel.orders.models import OrderDelivery
from portal.shop.models import ShopOrder, ShopOrderPayment


# Create your views here.

def orders_list(request):
	context = {}
	data = {}

	# context['total_products'] = context['store'].all().count()
	if request.is_ajax() and request.method == 'GET':

		context['form_search'] = SearchOrderForm(request.GET)

		if context['form_search'].is_valid():
			query = context['form_search'].cleaned_data['query']
			if query is not None:
				if query:
					lookups = Q(name__icontains=query)|Q(folio__icontains=query)|Q(order_payment__payment_intent__icontains=query)|Q(shop_order_delivery__tracking_number__icontains=query)
					context['orders_list'] = ShopOrder.objects.select_related('order_payment').filter(lookups)\
															.order_by('-created')
				else:
					context['orders_list'] = ShopOrder.objects.select_related('customer').filter(status=True).order_by('-created')

				if context['orders_list'].exists():
					data['search_valid'] = True
					data['html_orders'] = render_to_string('orders/includes/partial_orders_shop_list.html', context, request=request)
				else:
					data['search_valid'] = False
					data['message'] = 'Orden no encontrada'

				return JsonResponse(data)

	context['form_search'] = SearchStoreForm()

	page = request.GET.get('page',1)
	orders_list = ShopOrder.objects.select_related('customer').filter(status=True).order_by('-created')

	context['orders_list'] = pagination(orders_list,page,10)
	context['form_search'] = SearchOrderForm()


	return render(request,'orders/orders_list.html',context)


def orders_shop_products(request,order_pk):
	context = {}
	context['order'] = get_object_or_404(ShopOrder.objects.prefetch_related('products_orders', 'shop_order_delivery'), pk=order_pk)
	context['order_delivery'] = get_object_or_404(OrderDelivery, order=order_pk)
	orderShipping = get_object_or_404(ShopOrderPayment, order=order_pk)
	if request.method == 'POST':
		context['delivery_form'] = OrderDeliveryForm(request.POST, instance=context['order_delivery'])
		if context['delivery_form'].is_valid():
			context['company'] = context['delivery_form'].cleaned_data['delivery_company']
			context['tracking'] = context['delivery_form'].cleaned_data['tracking_number']
			context['range_date_start'] = context['delivery_form'].cleaned_data['range_date_start']
			context['range_date_end'] = context['delivery_form'].cleaned_data['range_date_end']
			context['delivery_order'] = context['delivery_form'].save()
			orderShipping.status = 'EE'
			orderShipping.save()
			# delivery_order.sendmail_order(request, context['order'])
			#-- Sendmail order to customer (From,to)
			context['request'] = request
			message = render_to_string('orders/includes/delivery_mail.html' ,context)
			sendmail('Tu pedido de %s n.º %s ha sido enviado' % ('Lunik', context['order'].folio), message, settings.DEFAULT_FROM_EMAIL,context['order'].email)
			return redirect('orders:orders_shop_products', order_pk=context['order'].pk)
	else:

		context['delivery_form'] = OrderDeliveryForm(instance=context['order_delivery'])
	return render(request,'orders/orders_products_list.html',context)

def orders_report_prints(self,campaing_pk):
	order_list = []
	context = {}
	data = []

	context['store'] = get_object_or_404(Store.objects.prefetch_related('shop_orders'), pk=campaing_pk)

	headers = ['Folio','Producto','Modelo','Imagen','Color','Talla','Total','Nombre','Numero','Tipo de envio','Dirección']

	for order in context['store'].shop_orders.filter(status=True):
		for product in order.products_orders.all().order_by('product','quantity'):
			data = tuple(
				(order.folio,
				product.product.product.product.name,
				product.product.product.product.model,
				product.product.image,
				product.product.color.hexacode.hexacode,
				product.size,
				product.quantity,
				product.name,
				product.number,
				'Envio a domicilio' if order.order_payment.shipping_option == 'HS' else 'Envio a escuela',
				'%s %s %s %s,USA.' % (order.order_delivery.address,order.order_delivery.zip_code,\
										order.order_delivery.city,order.order_delivery.state.name
									 ) if order.order_payment.shipping_option == 'HS' else None
				)
			)
			order_list.append(data)

	products_file = export_xls_file('Productos_campana_%s' %(context['store'].name),context['store'].name,headers,order_list)

	return products_file


def orders_shipping_status(request, order_pk):
	order = get_object_or_404(ShopOrder, pk=order_pk)
	try:
		orderShipping = ShopOrderPayment.objects.get(order=order_pk)
		if orderShipping.status == 'PE':
			orderShipping.status = 'EP'
			orderShipping.save()
			return redirect('orders:orders_shop_products', order_pk=order.pk)
		if orderShipping.status == 'EP':
			orderShipping.status = 'EE'
			orderShipping.save()
			return redirect('orders:orders_shop_products', order_pk=order.pk)
		if orderShipping.status == 'EE':
			orderShipping.status = 'EN'
			orderShipping.save()
			return redirect('orders:orders_shop_products', order_pk=order.pk)
	except ShopOrderPayment.DoesNotExist:
			order.status = False
			order.save()
			return redirect('orders:orders_list')
		



def orders_shop_sendmail(request,pk):

	order = get_object_or_404(ShopOrder.objects.select_related('store').prefetch_related('products_orders', 'shop_order_delivery'), pk=pk)

	data = OrderDelivery.sendmail_shop_link(request,order,'/panel/orders/','orders:orders_shop_sendmail')

	return JsonResponse(data)
