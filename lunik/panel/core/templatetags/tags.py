from django import template
from django.conf import settings
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from decimal import Decimal
from django.db.models import FileField, ImageField

#from panel.offers.models import Coupon

register = template.Library()

#-- Split Text with character given
def split_video(value, arg):
	text = value.split(arg)

	return text[4]

register.filter('splitvideo', split_video)

def range_count(min=1):
    value = int(min) + 1

    return range(1,value)

register.filter('range_count', range_count)

def instance_form_field(instance):
    field_list = []
    for field in instance._meta.get_fields():
        if field.name in instance.include_fields:
            field_name = str(field).split(".").pop()
            if isinstance(field,ImageField) or isinstance(field,FileField):
                field_list.append(format_html("<div class='mr-lg-3 mb-3 mb-lg-0'>\
			                                        <a href='{}{}' data-popup='lightbox'>\
			                                        <img src='{}{}' height='60'>\
			                                        </a></div>",settings.MEDIA_URL,getattr(instance, field_name)\
			                                    ,settings.MEDIA_URL,getattr(instance, field_name)
			                        			)
			                        )
            else:
                field_list.append(getattr(instance, field_name))

    return field_list

register.filter('instance_form_field',instance_form_field)

def instance_file_field(instance):
    files_list = []
    class_names = ['ManyToOneRel','ForeignKey','AutoField','ManyToManyField']
    for field in instance._meta.get_fields():
        field_class = field.__class__.__name__
        if field_class not in class_names:
            field_name = str(field).split(".").pop()
            if isinstance(field,FileField) or isinstance(field,ImageField):
                if getattr(instance, field_name) != '':
                	files_list.append(getattr(instance, field_name))

    return files_list

register.filter('instance_file_field', instance_file_field)

def coupon(product, coupon):
    if coupon:
        if coupon.products_coupons.filter(product=product).exists() or coupon.apply_all:
            return True
        else:
            return False
    else:
        return False
register.filter('coupon', coupon)

def get_quantity_cart(key,items):
    return items['variants'][key]['quantity']

register.filter('get_quantity_cart', get_quantity_cart)

def get_charge_price_cart(key,items):
    return items['price_charge'][key]

register.filter('get_charge_price_cart', get_charge_price_cart)

def get_custom_price_cart(key,items):
    return items['price_custom'][key]

register.filter('get_custom_price_cart', get_custom_price_cart)

def get_custom_name(key,items):
    return items['variants'][key]['name_personalization']

register.filter('get_custom_name', get_custom_name)

def get_custom_name_cart(key,items):
    name = items['variants'][key].get('name')
    number = items['variants'][key].get('number')

    return format_html('<b>Name:</b> {} - <b>Number:</b> {}',name,number)
    
register.filter('get_custom_name_cart', get_custom_name_cart)

def get_form_cart(key,items):
    return items['form_quantity'][key]['quantity']
    
register.filter('get_form_cart', get_form_cart)

def get_sizes_cart(key,items):
    return items['sizes'][key]

register.filter('get_sizes_cart', get_sizes_cart)

def get_price_after_discount(key, items):
    return items['variants'][key]['quantity'] * items['price_charge'][key]

register.filter('get_price_after_discount', get_price_after_discount)


def get_total_cart(key,items):
    total = 0

    if items.get('coupon') and items.get('coupon') is not None and not items.get('coupon').apply_all:
        discount = items['coupon'].discount
        price = items['totals'][key]
        if items['coupon'].discount_types == 'P':
            subtotal = (100 - Decimal(discount))/100 * Decimal(price)
            total = subtotal - total
        elif items['coupon'].discount_types == 'A':
            dis = price - discount
            if dis < 0:
                total = 0
            else:
                total = dis

        return total.__round__(2)
    else:

        return items['totals'][key]

register.filter('get_total_cart', get_total_cart)

def is_gift(key, item):
    if item['add_gift']:
        return True
    else:
        return False

register.filter('is_gift', is_gift)