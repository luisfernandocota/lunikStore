# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
	#-- List stores orders
    url(r'^$', views.orders_list, name='orders_list'),
    #-- Shop products print
    url(r'^shop/print/(?P<campaing_pk>[0-9]+)/$', views.orders_report_prints, name='orders_report_prints'),
    #-- Shop products list
    url(r'^shop/products/(?P<order_pk>[0-9]+)/$', views.orders_shop_products, name='orders_shop_products'),
	#-- Order sendmail
    url(r'^shop/sendmail/(?P<pk>[0-9]+)/$', views.orders_shop_sendmail, name='orders_shop_sendmail'),
    #-- Shop products list
    url(r'^shop/products/status/(?P<order_pk>[0-9]+)/$', views.orders_shipping_status, name='orders_shipping_status'),

]
