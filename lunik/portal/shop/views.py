# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import stripe


from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Max, Min

from panel.orders.models import OrderDelivery

from panel.products.models import Product, Coupon
from panel.website.models import Slide

from panel.core.utils import pagination

#from panel.offers.models import Coupon
#from panel.inventory.models import InventoryProduct
from .forms import ProductShopCart,ShopOrderForm,ShopOrderDeliveryForm, ContactForm
from .cart import Cart
from .models import ShopOrder,ShopOrderProduct,ShopOrderPayment
from portal.dashboard.models import Address

# Create your views here.

stripe.api_key = 'sk_test_51H5LaSIKF8Hi9Jx6yW3RzsyKlJDSLAcxolhL6C7g4G1PqjXUTdRfuhmnPap94WJn0q908PqVauxGBh3EHWykv90t00UkIeOM2P'

# Util view
def filters_by_request(request):
	filters = {}
	# params_category = request.GET.getlist('categoria')
	# params_subcategory = request.GET.get('subcategoria')
	param_shipping = request.GET.get('envio')
	param_is_sale = request.GET.get('oferta')
	param_price_min = request.GET.get('min')
	param_price_max = request.GET.get('max')
	param_search = request.GET.get('buscar')

	# if params_category:
	# 	category = {'product__subcategory__category__slug__in':params_category}
	# 	# queries.append(Q(product__subcategory__category__name__in=params_category))
	# 	filters.update(category)
	# if params_subcategory:
	# 	subcategory = {'product__subcategory__slug': params_subcategory}
	# 	filters.update(subcategory)
	if param_shipping:
		shipping = {'products_properties__shipping_free':True}
		filters.update(shipping)
	# 	queries.append(Q(shipping_free=True))
	if param_is_sale:
		is_sale = {'products_properties__is_sale':True}
		filters.update(is_sale)
	if param_price_max and param_price_min:
		price_range = {'products_properties__sell_price__range':(int(param_price_min), int(param_price_max))}
		filters.update(price_range)
	if param_search:
		search_name = {'name__icontains': param_search}
		# search_category = {'product__subcategory__category__name__icontains': param_search}
		filters.update(search_name)
		# filters.update(search_category)

	return filters

def shop_list(request):
	context = {}
	context['slides_list'] = Slide.objects.filter(status=True).order_by('-created')
	context['products_list'] = Product.objects.prefetch_related('products_properties').filter(available=True, status=True, products_properties__sell_price__gte=1).order_by('-created')

	return render(request,'shop/shop_list.html',context)

def products_list(request):
	context = {}

	filters = filters_by_request(request)



	if filters:
		products_list = Product.objects.select_related('products_properties').filter(available=True, status=True, products_properties__sell_price__gte=1).filter(**filters).order_by('-created')
	else:
		products_list = Product.objects.prefetch_related('products_properties').filter(available=True, status=True, products_properties__sell_price__gte=1).order_by('-created')

	# if store_products:
	if request.GET.get('min') and request.GET.get('max'):
		context['p_min_price'] = request.GET.get('min')
		context['p_max_price'] = request.GET.get('max')
	# context['min_price'] = int(context['store'].store_products.filter(status=True, product__available=True)\
	# 	.order_by('price').first().price)
	else:
		context['min_price'] = Product.objects.prefetch_related('products_properties').filter(available=True, status=True)\
						.aggregate(Min('products_properties__sell_price'))
		# context['max_price'] = int(context['store'].store_products.filter(status=True, product__available=True)\
		# 	.order_by('-price').first().price)
		context['max_price'] = Product.objects.prefetch_related('products_properties').filter(available=True, status=True)\
						.aggregate(Max('products_properties__sell_price'))
						
	context['min_price'] = Product.objects.prefetch_related('products_properties').filter(available=True, status=True)\
						.aggregate(Min('products_properties__sell_price'))
	context['max_price'] = Product.objects.prefetch_related('products_properties').filter(available=True, status=True)\
						.aggregate(Max('products_properties__sell_price'))
	context['products_count'] = Product.objects.prefetch_related('products_properties').filter(available=True, status=True).count()

	context['products'] = products_list
	page = request.GET.get('page', 1)
	context['products_list'] = pagination(products_list, page, 16)
	# context['products_colors'] = ProductHexaCodeM2M.objects.select_related('product')\
	# 	.filter(status=True, product=store_products.products)
	# context['products_sold'] = context['store'].total_products_sold()

	return render(request,'shop/products_list.html',context)

def categories_list(request):
	context = {}


	return render(request, 'shop/categories_list.html', context)

# @required_tenant
# def product_filter(request, category_slug):
# 	context = {}
# 	tenant = tenant_from_request(request)
# 	context['store'] = Store.store_validity(request, tenant)
# 	if context['store']:
# 		if not request.POST and category_slug == 'precio':
# 			return redirect('shop:products_list')
# 		else:
# 			# context['min_price'] = int(context['store'].store_products.filter(status=True, product__available=True)\
# 			# 	.order_by('price').first().price)
# 			context['min_price'] = context['store'].store_products.filter(status=True, product__available=True)\
# 				.aggregate(Min('price'))
# 			# context['max_price'] = int(context['store'].store_products.filter(status=True, product__available=True)\
# 			# 	.order_by('-price').first().price)
# 			context['max_price'] = context['store'].store_products.filter(status=True, product__available=True)\
# 				.aggregate(Max('price'))
# 			if category_slug != 'precio':
# 				if category_slug == 'oferta':
# 					store_products = context['store'].store_products.select_related('product', 'product__brand', 'product__subcategory')\
# 						.filter(status=True, product__available=True, is_sale=True).order_by('order')
# 				else:
# 					context['category'] = get_object_or_404(ProductCategory, slug=category_slug, store__pk=context['store'].pk)
# 					store_products = context['store'].store_products.select_related('product', 'product__brand', 'product__subcategory')\
# 						.filter(status=True, product__available=True, product__subcategory__category__slug=category_slug).order_by('order')
# 			if request.method == 'POST':
# 				min_price = request.POST.get('min_price')
# 				max_price = request.POST.get('max_price')
# 				store_products = context['store'].store_products.select_related('product', 'product__brand', 'product__subcategory')\
# 					.filter(status=True, product__available=True, price__range=(min_price, max_price)).order_by('price')
# 				context['filter_price'] = True
# 				context['min'] = min_price
# 				context['max'] = max_price
# 				context['products_count']  = store_products.count()
# 				context['products'] = store_products
# 			else:
# 				context['products_count'] = context['store'].store_products\
# 					.filter(status=True, product__available=True).count()
# 		context['products'] = store_products
# 		page = request.GET.get('page', 1)
# 		context['store_products'] = pagination(store_products, page, 9)
# 		# context['products_colors'] = ProductHexaCodeM2M.objects.select_related('product')\
# 		# 	.filter(status=True, product=store_products.products)
# 	# context['products_sold'] = context['store'].total_products_sold()

# 	return render(request,'shop/products_list.html',context)

def product_detail(request, slug):
	context = {}
	custom = {}

	context['product'] = get_object_or_404(Product.objects.prefetch_related('products_properties'),slug=slug, status=True, available=True)
	#context['inventory'] = get_object_or_404(InventoryProduct.objects.select_related('product').prefetch_related('product'), product=context['product'].product)
	#context['related_products'] = context['store'].store_products.select_related('product').exclude(product__slug=slug).filter(product__available=True).order_by('-created')[:4]
	if request.POST:

		context['form_product'] = ProductShopCart(request.POST,product_sizes=context['product'].sizes.all(), product_pk=context['product'].pk)
		if context['form_product'].is_valid():
			#-- Initialite cart
			cart = Cart(request)
			#-- Personalization design
			if context['form_product'].cleaned_data['name_personalization']:
				custom['name_personalization'] = context['form_product'].cleaned_data.get('name_personalization',None)

			#-- Extra sizes
			if context['form_product'].cleaned_data['sizes'].charge:
				custom['charge_size'] = context['form_product'].cleaned_data['sizes'].charge
			# design = get_object_or_404(StoreGallery, pk=context['form_product'].cleaned_data['design'])
			cart.add(context['product'],context['form_product'].cleaned_data['sizes'],context['form_product'].cleaned_data['quantity'],context['form_product'].cleaned_data['name_personalization'])
			return redirect('shop:product_detail', slug)

	else:
		context['form_product'] = ProductShopCart(initial={'product_pk':context['product'].pk},product_sizes=context['product'].sizes.all(), product_pk=context['product'].pk)


	return render(request,'shop/product_detail.html',context)

def cart_update(request):
	data = {}
	context = {}

	if request.method == 'GET':
		context['cart'] = Cart(request)

		product = get_object_or_404(Product, pk=request.GET.get('product_pk'))
		context['cart'].add(product,request.GET.get('size'),request.GET.get('quantity'),request.GET.get('total_quantity'))
		print(context['cart'].get_shipping_cost())
		data['form_is_valid'] = True
		data['html_cart_charge'] = render_to_string('shop/includes/partial_cart_charge.html',context)
		data['html_cart_table'] = render_to_string('shop/includes/partial_cart_table.html',context,request)
	return JsonResponse(data)

# @required_tenant
# def cart_shipping(request):
# 	data = {}
# 	context = {}
# 	tenant = tenant_from_request(request)
# 	context['store'] = Store.store_validity(request,tenant)
# 	if not request.user.is_superuser and not request.user.is_anonymous and request.user.is_customer:
# 		if request.user.phone:
# 			context['form_order'] = ShopOrderForm(
# 				initial={
# 					'name': request.user.get_full_name(),
# 					'email': request.user.email,
# 					'phone': request.user.phone,
# 					}
# 				)
# 		else:
# 			context['form_order'] = ShopOrderForm(
# 				initial={
# 					'name': request.user.get_full_name(),
# 					'email': request.user.email,
# 					}
# 				)
# 		try:
# 			address = Address.objects.get(default=True, status=True, user=request.user)
# 			context['form_delivery'] = ShopOrderDeliveryForm(
# 				initial={
# 					'address': address.address,
# 					'num_ext': address.num_ext,
# 					'num_int': address.num_int,
# 					'suburb': address.suburb,
# 					'zip_code': address.zip_code,
# 					'city': address.city,
# 					'state': address.state,
# 					}
# 			)
# 		except Address.DoesNotExist:
# 			context['form_delivery'] = ShopOrderDeliveryForm()
# 	else:
# 		context['form_order'] = ShopOrderForm()
# 		context['form_delivery'] = ShopOrderDeliveryForm()

# 	if request.is_ajax() and request.method == 'GET':
# 		context['cart'] = Cart(request)
# 		# context['cart'].get_shipping_cost(shipping=request.GET.get('shipping'),limit=request.GET.get('limit'),
# 		# 								extra=request.GET.get('extra')
# 		# 								)

# 		data['form_is_valid'] = True

# 		data['html_cart_checkout'] = render_to_string('shop/includes/partial_cart_checkout.html',context,request)

# 		return JsonResponse(data)

def cart_remove(request):
	data = {}
	context = {}
	if request.is_ajax() and request.method == 'GET':
		product = get_object_or_404(Product, pk=request.GET.get('product'))
		size = request.GET.get('size')

		context['cart'] = Cart(request)
		context['cart'].remove(product,size)
		data['form_is_valid'] = True

		if request.GET.get('checkout') == '1':
			data['checkout'] = True

		data['html_cart_charge'] = render_to_string('shop/includes/partial_cart_charge.html',context)
		data['html_cart_table'] = render_to_string('shop/includes/partial_cart_table.html',context,request)
		return JsonResponse(data)

def cart_address(request):
	data = {}
	context = {}
	if request.is_ajax() and request.method == 'POST':
		context['step'] = request.POST.get('step')
		data['step'] = request.POST.get('step')
		context['form_order'] = ShopOrderForm(request.POST)
		context['form_delivery'] = ShopOrderDeliveryForm(request.POST)
		if context['form_order'].is_valid() and context['form_delivery'].is_valid():
			data['form_is_valid'] = True
			context['cart'] = Cart(request)
			context['cart'].add_address(order=context['form_order'], delivery=context['form_delivery'])
		else:
			data['form_is_valid'] = False
			context['form_order'] = ShopOrderForm(request.POST)
			context['form_delivery'] = ShopOrderDeliveryForm(request.POST)
			data = {'errors':[]}
			errors = data['errors']
			for field in context['form_order']:
				for error in field.errors:
					errors.append({'field': field.name, 'error': error})
			for field in context['form_delivery']:
				for error in field.errors:
					errors.append({'field': field.name, 'error': error})
		data['html_dynamic'] = render_to_string('shop/includes/partial_dynamic_checkout.html',context,request)
		data['html_footer'] = render_to_string('shop/includes/partial_footer_checkout.html',context,request)
	
	return JsonResponse(data)

def cart_detail(request):
	context = {}

	return render(request,'shop/shop_cart.html',context)
	
@csrf_exempt
def cart_checkout(request):
	context = {}
	data = {}
	context['step'] = request.GET.get('step')

	context['cart'] = Cart(request)
	if context['cart'].get_quantity_products() > 0:
		if not request.user.is_superuser and not request.user.is_anonymous and request.user.is_customer:
			if request.user.phone:
				context['form_order'] = ShopOrderForm(
					initial={
						'name': request.user.get_full_name(),
						'email': request.user.email,
						'phone': request.user.phone,
						}
					)
			else:
				context['form_order'] = ShopOrderForm(
					initial={
						'name': request.user.get_full_name(),
						'email': request.user.email,
						}
					)
			try:
				address = Address.objects.get(default=True, status=True, user=request.user)
				context['form_delivery'] = ShopOrderDeliveryForm(
					initial={
						'address': address.address,
						'num_ext': address.num_ext,
						'num_int': address.num_int,
						'suburb': address.suburb,
						'zip_code': address.zip_code,
						'city': address.city,
						'state': address.state,
						}
				)
			except Address.DoesNotExist:
				context['form_delivery'] = ShopOrderDeliveryForm()
		else:
			if context['cart'].get_address_order():
				context['form_order'] = ShopOrderForm(None,initial=context['cart'].get_address_order())
			if context['cart'].get_address_delivery():
				context['form_delivery'] = ShopOrderDeliveryForm(None,initial=context['cart'].get_address_delivery())
			else:
				context['form_order'] = ShopOrderForm(None)
				context['form_delivery'] = ShopOrderDeliveryForm(None,)
	
		if request.is_ajax() and request.method == 'GET':

			context['step'] = request.GET.get('step')
			data['html_dynamic'] = render_to_string('shop/includes/partial_dynamic_checkout.html',context,request)
			data['html_footer'] = render_to_string('shop/includes/partial_footer_checkout.html',context,request)
			return JsonResponse(data)
		if request.method == 'POST':
			form_order = ShopOrderForm(request.POST, initial=context['cart'].get_address_order())
			form_delivery = ShopOrderDeliveryForm(request.POST, initial=context['cart'].get_address_delivery())
			# if context['form_order'].is_valid() and context['form_delivery'].is_valid():

			try:
				# Create a PaymentIntent with the order amount and currency
				intent = stripe.PaymentIntent.create(
					amount=context['cart'].get_total_products_stripe(),
					currency='mxn',
					automatic_payment_methods={
						'enabled': True,
					},
				)
				return JsonResponse({
					'clientSecret': intent['client_secret']
				})
			except Exception as e:
				return JsonResponse(error=str(e)), 403	
			# try:
			# 	#-- Stripe payment
			# 	stripe.api_key = 'sk_test_51H5LaSIKF8Hi9Jx6yW3RzsyKlJDSLAcxolhL6C7g4G1PqjXUTdRfuhmnPap94WJn0q908PqVauxGBh3EHWykv90t00UkIeOM2P'
			# 	token = request.POST.get('stripeToken')
			# 	charge = stripe.Charge.create(
			# 		amount=context['cart'].get_total_products_stripe(),
			# 		currency='mxn',
			# 		description='%s-%s' % (context['store'].name,context['store'].code),
			# 		source=token,
			# 	)
			# 	#-- payment successful
			# 	if charge['paid']:
			# 		#-- Save order in DB
			# 		order = form_order.save(commit=False)
			# 		order.store = context['store']
			# 		if not request.user.is_superuser and not request.user.is_anonymous and request.user.is_customer:
			# 			order.customer = request.user
			# 		order.date_order = timezone.now().today()
			# 		order.save()

			# 		# if context['form_delivery'].has_changed():
			# 		delivery = form_delivery.save(commit=False)
			# 		delivery.order = order
			# 		delivery.save()

			# 		#-- Save products from order
			# 		order_products = ShopOrderProduct.products_save(context['cart'],order)
			# 		ShopOrderProduct.objects.bulk_create(order_products)
			# 		#-- Create OrderDelivery objetc
			# 		#OrderDelivery.objects.create(order=order)
			# 		#-- Save payment from order
			# 		payment = ShopOrderPayment(
			# 						order = order,
			# 						stripe_folio = charge['id'],
			# 						total = context['cart'].get_subtotal_products(),
			# 						shipping = context['cart'].get_shipping_cost(),
			# 					)
			# 		if context['cart'].is_coupon_apply():
			# 			#coupon = Coupon.objects.get(pk=context['cart'].is_coupon_apply().pk)
			# 			#coupon.uses += 1
			# 			#coupon.save()
			# 			#payment.coupon = coupon
						
			# 			payment.save()

			# 		#--Purchase informarion
			# 		context['folio'] = order.folio
			# 		context['email'] = order.email
			# 		context['store_name'] = context['store'].name

			# 		#-- Sendmail from order
			# 		ShopOrder.sendmail_order(request, order, info)

			# 		#-- Delete cart session
			# 		#context['cart'].clear()
			# 		del request.session[settings.CART_COOKIE_NAME]

			# 		#return render(request,'shop/shop_payment_successful.html',context)
			# 		context['order'] = order
			# 		return render(request,'shop/shop_payment_successful.html',context)

			# except stripe.error.CardError:
			# 		return render(request,'shop/shop_payment_error.html',context)
		return render(request,'shop/shop_checkout.html',context)
	else:
		return redirect('shop:cart_detail')

def retrievePayment(request):
	data = {}
	context = {}
	cart = Cart(request)
	body = json.loads(request.body)

	exists = ShopOrder.objects.filter(order_payment__payment_intent=body['paymentIntent']['id']).exists()
		
	if request.method == 'POST' and exists == False:
		form_order = ShopOrderForm(data=cart.get_address_order(), initial=cart.get_address_order())
		form_delivery = ShopOrderDeliveryForm(data=cart.get_address_delivery(), initial=cart.get_address_delivery())
		if body['paymentIntent']['status'] == 'succeeded':
			if form_order.is_valid() and form_delivery.is_valid():
				#-- Save order in DB
				order = form_order.save(commit=False)
				if not request.user.is_superuser and not request.user.is_anonymous and request.user.is_customer:
					order.customer = request.user
				order.save()
				delivery = form_delivery.save(commit=False)
				delivery.order = order
				delivery.save()

				#-- Save products from order
				order_products = ShopOrderProduct.products_save(cart,order)
				ShopOrderProduct.objects.bulk_create(order_products)
				#-- Create OrderDelivery objetc
				OrderDelivery.objects.create(order=order)
				#-- Save payment from order
				payment = ShopOrderPayment(
								order = order,
								payment_intent = body['paymentIntent']['id'],
								client_secret = body['paymentIntent']['client_secret'],
								total = cart.get_subtotal_products(),
								shipping = cart.get_shipping_cost(),
							)
				if cart.is_coupon_apply():
					coupon = Coupon.objects.get(pk=cart.is_coupon_apply().pk)
					coupon.uses += 1
					coupon.save()
					payment.coupon = coupon
						
				payment.save()
				
				#--Purchase informarion
				context['folio'] = order.folio
				context['email'] = order.email

				data['html_succeeded'] = render_to_string('shop/includes/partial_payment_succeeded.html',context,request)
				#-- Delete cart session
				del request.session[settings.CART_COOKIE_NAME]

			
		
	else:

		data['exists'] = True
		data['url_redirect'] = '/'
	return JsonResponse(data)



def cartPaymentIntent(request):
	context = {}

	return render(request, 'shop/order_payment.html', context)

def info(request):
	context = {}

	return render(request, 'shop/about_us.html', context)

def contact(request):
	context = {}
	#context['offices_list'] = Office.objects.filter(status=True, store_meta__store__customer__tenant=tenant)
	obj = context['offices_list'].first()
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()

			message = render_to_string('shop/includes/contact_mail.html', {
									'name' : form.cleaned_data.get('name'),
									'email': form.cleaned_data.get('email'),
									'phone': form.cleaned_data.get('phone'),
									'comment' : form.cleaned_data.get('comment'),
									'obj' : obj,
									'request': request,
									})

			subject = '%s :: Contacto' %(context['offices_list'].first().store_meta.store)
			context['success'] = True
			#sendmail(subject, message, settings.DEFAULT_FROM_EMAIL, context['offices_list'].first().store_meta.info.email_store)

			return render(request, 'shop/contact.html', context)
	else:
		context['contact_form'] = ContactForm()
	return render(request, 'shop/contact.html', context)

def resend_mail(request, pk):
	data = {}
	context = {}
	#info = get_object_or_404(Info, store_meta__store=context['store'])

	if request.is_ajax() and request.method == 'GET':
		order = get_object_or_404(ShopOrder, pk=pk)
		ShopOrder.sendmail_order(request, order, info)

		data['form_is_valid'] = True

		return JsonResponse(data)

def apply_coupon(request):
	#from panel.offers.models import Coupon
	data = {}
	context = {}
	data['coupon_404'] = False
	data['is_products_in_coupon'] = True


	if request.is_ajax() and request.method == 'GET':
		try:
			if request.GET.get('coupon'):
				context['coupon'] = Coupon.objects.get(code__exact=request.GET.get('coupon'), available=True, status=True)
				context['cart'] = Cart(request)
				context['applied'] = context['cart'].apply_coupon(context['coupon'])

				if context['applied']:

					data['coupon_is_valid'] = True
					data['html_cart_coupon'] = render_to_string('shop/includes/partial_cart_coupon.html',context,request)
					data['html_cart_charge'] = render_to_string('shop/includes/partial_cart_charge.html',context)
					data['html_cart_table'] = render_to_string('shop/includes/partial_cart_table.html',context,request)
				else:
					if not context['cart'].is_products_in_coupon():
						data['is_products_in_coupon'] = False
					elif context['cart'].get_subtotal_products() < context['coupon'].min_purchase:
						data['min_purchase'] = False
						data['min_purchase_msg'] = 'Para usar este cupón debes de hacer una compra mínima de $%s' % context['coupon'].min_purchase
					else:
						data['coupon_is_valid'] = False
			else:
				data['coupon_empty'] = True
				data['coupon_404'] = True

		except:
			data['coupon_404'] = True

	return JsonResponse(data)

def del_coupon(request):
	data = {}
	context = {}

	if request.is_ajax() and request.method == 'GET':

		context['cart'] = Cart(request)
		context['cart'].del_coupon()

		data['form_is_valid'] = True

		data['html_cart_coupon'] = render_to_string('shop/includes/partial_cart_coupon.html',context,request)
		data['html_cart_table'] = render_to_string('shop/includes/partial_cart_table.html',context,request)
		data['html_cart_charge'] = render_to_string('shop/includes/partial_cart_charge.html',context)

		return JsonResponse(data)

