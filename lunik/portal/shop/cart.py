#-*- coding: utf-8 -*-

from decimal import Decimal
from django.conf import settings
import datetime

from panel.products.models import Product

class Cart(object):

	#-- Init cart session
	def __init__(self,request,campaign=None):
		self.session = request.session

		cart = self.session.get(settings.CART_COOKIE_NAME)

		if not cart:
			cart = self.session[settings.CART_COOKIE_NAME] = {'shop':{},'shipping':{}, 'address':{'order':{}, 'delivery': {}}}

		self.local = (40).__round__(2)
		self.cart = cart

		self.save()

	#-- Add or update cart session
	def add(self,product,size,quantity,custom=None, gift=None):
		product_pk = str(product.pk)
		product_size = str(size)
		if product_pk not in self.cart['shop']:
			#self.cart['shop'][product_pk] = {'variants':{product_size:0},'price':str(design.product.price)}
			if product.products_properties.is_sale:
				self.cart['shop'][product_pk] = {'variants':{product_size:{}},'price':str(product.products_properties.sale_price)}
			else:
				self.cart['shop'][product_pk] = {'variants':{product_size:{}},'price':str(product.products_properties.sell_price)}
			if custom['name_personalization']:
				self.cart['shop'][product_pk]['variants'][product_size]= {'name_personalization':{custom['name_personalization']:{}}}
				self.cart['shop'][product_pk]['variants'][product_size]['name_personalization'][custom['name_personalization']] = {'quantity': 1}
			self.cart['shop'][product_pk]['variants'][product_size]['quantity'] = int(quantity)
			if product.products_properties.shipping_min is not None:
				self.cart['shop'][product_pk]['variants'][product_size]['shipping_limit'] = int(product.products_properties.shipping_min)
			else:
				self.cart['shop'][product_pk]['variants'][product_size]['shipping_limit'] = 0
			if product.products_properties.shipping_price is not None:
				self.cart['shop'][product_pk]['variants'][product_size]['shipping'] = Decimal(product.products_properties.shipping_price)
			else:
				self.cart['shop'][product_pk]['variants'][product_size]['shipping'] = 0
			if gift:
				self.cart['shop'][product_pk]['variants'][product_size]['gift'] = gift
		else:
			if product_size not in self.cart['shop'][product_pk]['variants']:
				#self.cart['shop'][product_pk]['variants'].update({product_size:0})
				self.cart['shop'][product_pk]['variants'].update(
						{product_size:{
							'name_personalization':{custom['name_personalization']:{'quantity': 1}} if custom else None, 
							'quantity':int(quantity),
							'shipping_limit': int(product.products_properties.shipping_min),
							'shipping': Decimal(product.products_properties.shipping_price),

							}
						}
					)
			else:
				if custom['name_personalization']:
					self.cart['shop'][product_pk]['variants'][product_size]['quantity'] += 1
					if  custom['name_personalization'] not in self.cart['shop'][product_pk]['variants'][product_size]['name_personalization'].keys():
						self.cart['shop'][product_pk]['variants'][product_size]['name_personalization'][custom['name_personalization']] = {'quantity': 1}

					else:
						for k in self.cart['shop'][product_pk]['variants'][product_size]['name_personalization'].keys():

							if custom['name_personalization'] == k:

								self.cart['shop'][product_pk]['variants'][product_size]['name_personalization'][k]['quantity'] += 1
					# seq = int(self.cart['seq'].get('num','1'))

					# self.cart['shop'][product_pk]['variants'].update(
					# 	{'%s-%s'%(product_size,str(seq)):{
					# 		'name_personalization':custom, 
					# 		'quantity':int(quantity),
					# 		'shipping_limit': int(product.products_properties.shipping_min),
					# 		'shipping': Decimal(product.products_properties.shipping_price),

					# 		}
					# 	}
					# )
					# seq += 1
					# self.cart['seq']['num'] = str(seq)
		#self.cart['shop'][product_pk]['variants'][product_size] = int(product_quantity)
		
		self.save()

	#-- Save cart session
	def save(self):
		self.session[settings.CART_COOKIE_NAME] = self.cart
		self.session.modified = True

	#-- Remove product from cart session
	def remove(self,product,size):
		product_pk = str(product.pk)

		if product_pk in self.cart['shop']:
			del self.cart['shop'][product_pk]['variants'][size]

			if not self.cart['shop'][product_pk]['variants']:
				del self.cart['shop'][product_pk]
			if not self.is_products_in_coupon() or self.get_subtotal_products() < self.cart['coupon'].min_purchase:
				if self.cart.get('coupon_apply', False):
					del self.cart['coupon']
					del self.cart['coupon_apply']
					if self.cart.get('check_all', False):
						del self.cart['check_all']
					if self.cart.get('check_any', False):
						del self.cart['check_any']
			if not self.cart['shop']:
				try:
					# del self.cart['shipping']
					self.cart['shipping'].clear()
					self.cart['address']['order'].clear()
					self.cart['address']['delivery'].clear()
					if self.cart.get('coupon_apply', False):
						del self.cart['coupon']
						del self.cart['coupon_apply']
						if self.cart.get('check_all', False):
							del self.cart['check_all']
						if self.cart.get('check_any', False):
							del self.cart['check_any']
				except KeyError:
					pass
			self.save()

	#-- Iter products in cart session
	def __iter__(self):
		from django.db.models import Max
		products_keys = self.cart['shop'].keys()

 		# get the product objects and add them to the cart
		products = Product.objects.prefetch_related('products_properties').filter(pk__in=products_keys).order_by('-created')
		#products = Product.objects.select_related('product').filter(pk__in=products_keys).order_by('order')
		if self.cart.get('shipping'):
			self.cart['shipping'].get('total', 0)
		for item in products:
			self.cart['shop'][str(item.pk)]['product'] = item
			if item.products_properties.is_sale:
				self.cart['shop'][str(item.pk)]['temp_charge'] = str(item.products_properties.sale_price)
			else:
				self.cart['shop'][str(item.pk)]['temp_charge'] = str(item.products_properties.sell_price)
		for item in self.cart['shop'].values():
			item['sizes'] = {}
			item['totals'] = {}
			item['price_charge'] = {}
			item['price_custom'] = {}
			item['add_gift'] = {}
			#item['coupon'] = self.is_product_in_coupon(item['product'].pk)

			variants_keys = item['variants'].keys()
			
			for key in variants_keys:
				if item['variants'][key].get('gift'):
					item['add_gift']['gift_price'] = 20
				item['variants'][key] = item['variants'][key]
				item['sizes'][key] = key
				item['price_custom'][key] = item['variants'][key].get('charge_custom',0.00)
				item['price_charge'][key] = (Decimal(item['temp_charge']) + Decimal(item['variants'][key].get('charge_size',0.00)))
				#item['totals'][key] = item['variants'][key] * Decimal(item['price'])
				
				item['totals'][key] = (
										item['variants'][key]['quantity'] * Decimal(item['price']) +
										Decimal(item['variants'][key].get('charge_custom',0.00)) +
										item['variants'][key]['quantity'] * Decimal(item['variants'][key].get('charge_size',0.00)) +
										Decimal(item['add_gift'].get('gift_price', 0.00))
									  )

				if self.cart.get('shipping'):
					total = self.cart['shipping'].get('total')
				else:
					total = 0
				if item['product'].products_properties.shipping_free:

					if self.cart['shipping'].get('total') == 0:
						total = 0
					elif len(self.cart['shop'].values()) == 1:
						total = 0
				else:

					if item['variants'][key]['quantity'] >= item['variants'][key].get('shipping_limit',0):
						if self.all_shipping_free(products_keys):
							total = 0

					else:

						if item['variants'][key]['shipping'] > total:
							total = item['variants'][key]['shipping']
						else:
							total = item['variants'][key]['shipping']
							# self.cart['shipping']['total'] = Decimal(item['variants'][key]['shipping'])
			# if self.cart.get('shipping'):
			# 	if self.cart['shipping'].get('total'):
			self.cart['shipping']['shipping_total'] = total
			if total > 0:
				if self.cart['shipping'].get('method'):
					if self.cart['shipping']['method'] == 'nacional':
						self.cart['shipping']['total'] = total
					if self.cart['shipping']['method'] == 'local':
						self.cart['shipping']['total'] = 40
					if self.cart['shipping']['method'] == 'default':
						self.cart['shipping']['total'] = 0
				else:
					self.cart['shipping']['total'] = 0
			else:
				self.cart['shipping']['total'] = 0
			yield item


	#-- Clear Session
	def clear(self):
		# remove cart from session
		del self.session[settings.CART_COOKIE_NAME]
		self.session.modified = True

	#-- Quantity of products
	def get_quantity_products(self):
		total = 0
		for item in self.cart['shop'].values():
			for itemv in item['variants'].values():
				total += itemv['quantity']
			#total += sum(item for item in item['variants'].values())

		return total


	def all_shipping_free(self, products_keys):
		total = 0
		lenght = len(products_keys)
		for item in self.cart['shop'].values():
			variants_keys = item['variants'].keys()
			for key in variants_keys:
				if item['variants'][key]['quantity'] >= item['variants'][key].get('shipping_limit',0) or item['variants'][key].get('shipping_free',0):
					total += 1
		if total == lenght:
			return True
		else:
			return False
	#-- APPLY COUPON
	def apply_coupon(self, coupon):
		self.cart['coupon'] = coupon
		coupon_apply = self.cart.get('coupon_apply', False)
		# Program to check the list contains elements of another list
		total = 0
		keys = []
		cp = []
		# coupon_products = coupon.products_coupons.values_list('product__pk', flat=False)
		if coupon.no_uses > coupon.uses and coupon.date_expiration > datetime.date.today() and self.get_subtotal_products() >= coupon.min_purchase or coupon.min_purchase == 0:

			if  coupon.apply_all:
				coupon_apply = True
				self.cart['coupon_apply'] = coupon_apply
				self.cart['check_all'] = True
				return self.cart['coupon_apply']
			else:
				for p in coupon.products_coupons.all():
					cp.append(str(p.product.pk))
				for key in self.cart['shop'].keys():
					keys.append(key)

				check_all = all(item in keys for item in cp)
				check_any =  any(item in keys for item in cp)

				if check_all:
					self.cart['check_all'] = True
					coupon_apply = True
					self.cart['coupon_apply'] = coupon_apply
					return True

				elif check_any:
					self.cart['check_any'] = True

					coupon_apply = True
					self.cart['coupon_apply'] = coupon_apply
					return True
		else:
			return False

	def is_coupon_apply(self):
		if self.cart.get('coupon_apply', False):
			return self.cart['coupon']

	def get_subtotal_by_coupon(self):
		total = 0
		temp_total = 0
		discount = 0
		cp = []

		for item in self.cart['shop'].values():
			item['coupon'] = {}
			variants_keys = item['variants'].keys()
			for key in variants_keys:
				discount = self.cart['coupon'].discount
				#total += item['variants'][key] * Decimal(item['price'])
				total += (
							item['variants'][key]['quantity'] * Decimal(item['price']) +
							Decimal(item['variants'][key].get('charge_custom',0.00)) +
							item['variants'][key]['quantity'] * Decimal(item['variants'][key].get('charge_size',0.00))
						)
		if self.cart.get('check_any', False) or self.is_products_in_coupon() != len(self.cart['shop'].values()):
			for item in self.cart['shop'].values():
				for p in self.cart['coupon'].products_coupons.filter(product=item['product']):
					cp.append(str(p.product.pk))
			products_store = Product.objects\
									.filter(pk__in=cp).order_by('-created')
			for product in products_store:
				for item in self.cart['shop'].values():
					variants_keys = item['variants'].keys()

					for key in variants_keys:
						if item['product'] == product:
							if product.products_properties.is_sale:
								temp_total += (
												item['variants'][key]['quantity'] * Decimal(item['product'].products_properties.sale_price) +
												Decimal(item['variants'][key].get('charge_custom',0.00)) +
												item['variants'][key]['quantity'] * Decimal(item['variants'][key].get('charge_size',0.00)) +
												Decimal(item['add_gift'].get('gift_price', 0.00))
											)
								# temp_total += product.sale_price
							else:
								temp_total += (
												item['variants'][key]['quantity'] * Decimal(item['price']) +
												Decimal(item['variants'][key].get('charge_custom',0.00)) +
												item['variants'][key]['quantity'] * Decimal(item['variants'][key].get('charge_size',0.00)) +
												Decimal(item['add_gift'].get('gift_price', 0.00))
											)

			if self.cart['coupon'].discount_types == 'P':
				if temp_total > 0:

					temp = total - Decimal(temp_total)
					temp_subtotal = (100 - Decimal(discount))/100 * Decimal(temp_total)

					total = Decimal(temp) + Decimal(temp_subtotal)

				else:
					subtotal = Decimal(discount/100) * Decimal(total)
					total = total - Decimal(subtotal)
			elif self.cart['coupon'].discount_types == 'A':
				if temp_total > 0:
					temp = total - temp_total
					temp_subtotal = temp_total - Decimal(discount)
					dis = temp + temp_subtotal

				else:
					dis = total - Decimal(discount)
				if dis < 0:
					total = 0
				else:
					total = dis
		elif self.cart.get('check_all', False):

			if self.cart['coupon'].discount_types == 'P':
				subtotal = (100 - Decimal(discount))/100 * Decimal(total)

				total = total - Decimal(subtotal)

			elif self.cart['coupon'].discount_types == 'A':
				dis = total - Decimal(discount)
				if dis < 0:
					total = 0
				else:
					total = dis
		return total.__round__(2)

	def is_products_in_coupon(self):
		cp = []
		if self.cart.get('coupon', False):
			if not self.cart['coupon'].apply_all:
				for item in self.cart['shop'].values():
					cp.append(str(item['product'].pk))
				exist = self.cart['coupon'].products_coupons.filter(product__pk__in=cp).count()

				return exist
			else:
				#return True
				return 0

		#return False
		return 0

	def is_product_in_coupon(self, product_pk):
		if self.cart.get('coupon', False):
			exist = self.cart['coupon'].products_coupons.filter(product__pk=product_pk).exists()
			if exist:
				return self.cart['coupon']
			else:
				return False
	def del_coupon(self):
		if self.cart.get('coupon_apply', False):
			del self.cart['coupon']
			del self.cart['coupon_apply']
			if self.cart.get('check_all', False):
				del self.cart['check_all']
			if self.cart.get('check_any', False):
				del self.cart['check_any']
			self.save()



	#-- Total of products
	def get_subtotal_products(self):
		total = 0
		if self.cart.get('coupon_apply', False):
			total = self.get_subtotal_by_coupon()
		else:
			for item in self.cart['shop'].values():
				variants_keys = item['variants'].keys()
				for key in variants_keys:
					#total += item['variants'][key] * Decimal(item['price'])
					total += (
								item['variants'][key]['quantity'] * Decimal(item['price']) +
								Decimal(item['variants'][key].get('charge_custom',0.00)) +
								item['variants'][key]['quantity'] * Decimal(item['variants'][key].get('charge_size',0.00)) +
								Decimal(item['add_gift'].get('gift_price', 0.00))
							)

		return total

	def set_shipping_method(self, method):
		
		if self.cart.get('shipping'):
			if method == 'default':
				self.cart['shipping']['total'] = 0

			if method == 'local':

				self.cart['shipping']['total'] = self.local


			self.cart['shipping']['method'] = method
		self.save()
		
	def get_shipping_method(self):
		if self.cart.get('shipping'):
			if self.cart['shipping'].get('method'):
				return self.cart['shipping']['method']
			else:
				return False
		else:
			return False


	#-- Shipping cost of products
	def get_shipping_cost(self):
		if self.cart.get('shipping'):
			if self.get_subtotal_products() < 1999:
				return self.cart['shipping']['total']
			else:
				return 0
		else:
			return 0

	def get_shipping_total(self):
		if self.cart.get('shipping'):
			if self.get_subtotal_products() < 1999:
				return self.cart['shipping']['shipping_total']
			else:
				return 0
		else:
			return 0
		

	#-- Total of products
	def get_total_products(self):
		total = self.get_subtotal_products() + self.get_shipping_cost()

		return total

	#-- Total of products
	def get_total_products_stripe(self):
		if self.cart.get('shop'):
			g = self.get_subtotal_products() + self.get_shipping_cost()
			h = str(g).split('.')
			total = h[0] + h[1]
			return total

	# Set address in cache cart
	def add_address(self, *args,**kwargs):
		order_form = kwargs.pop('order')
		delivery_form = kwargs.pop('delivery')
		# range_code = range(81200,81394)
		for field in order_form:
			self.cart['address']['order'][field.name] = order_form.cleaned_data[field.name]
		for field in delivery_form:
			self.cart['address']['delivery'][field.name] = delivery_form.cleaned_data[field.name]

	def get_address_order(self):
		if self.cart.get('address'):
			if self.cart['address'].get('order'):
				return self.cart['address']['order']
			else:
				return False
		else:
			return False
	def get_address_delivery(self):
		if self.cart.get('address'):
			if self.cart['address'].get('delivery'):
				return self.cart['address']['delivery']
			else:
				return False
		else:
			return False
	def get_email_by_address(self):
		if self.cart['address']['order'].get('email'):
			return '%s' % self.cart['address']['order']['email']
		else:
			return False
	def get_street_by_address(self):
		if self.cart['address']['delivery'].get('address') and \
			self.cart['address']['delivery'].get('num_ext') and \
			self.cart['address']['delivery'].get('city') and \
			self.cart['address']['delivery'].get('state'):
			return '%s #%s %s, %s' % (
				self.cart['address']['delivery']['address'], 
				self.cart['address']['delivery']['num_ext'], 
				self.cart['address']['delivery']['city'],
				self.cart['address']['delivery']['state'])
		else:
			return False

	def get_suburb_by_address(self):
		if self.cart['address'].get('delivery'):
			return self.cart['address']['delivery']['suburb']
		else:
			return False	