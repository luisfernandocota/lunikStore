# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    #-- Shop products list
    path('', views.shop_list, name='shop_list'),
    #-- Products list
    path('productos/', views.products_list, name='products_list'),
    #-- Categories list
    path('categorias/', views.categories_list, name='categories_list'),
    #-- Product Detail
    path('detalle/<slug:slug>', views.product_detail, name='product_detail'),
    # #-- Product by category
    # path('productos/categoria/<slug:category_slug>', views.product_filter, name='product_filter'),
    #-- Cart detail
    path('carrito/', views.cart_detail, name='cart_detail'),
    #-- Cart checkout
    path('carrito/checkout/', views.cart_checkout, name='cart_checkout'),
    #-- Retrieve Payment
    path('carrito/checkout/retrievePayment/', views.retrievePayment, name='retrievePayment'),
    #-- Cart add address
    path('cart/add_address/', views.cart_address, name='cart_address'),
    #-- Update product to cart
    path('cart/update/', views.cart_update, name='cart_update'),
    #-- Update shipping to cart
    # path('cart/shipping/', views.cart_shipping, name='cart_shipping'),
    #-- Remove product to cart
    path('cart/remove/', views.cart_remove, name='cart_remove'),
    #-- Apply coupon
    path('cart/apply_coupon/', views.apply_coupon, name='apply_coupon'),
    #-- Remove coupon to cart
    path('cart/coupon/remove/', views.del_coupon, name='del_coupon'),

    #-- Cart Payment Intent
    path('order/', views.cartPaymentIntent, name="cartPaymentIntent"),

    #-- Resend Mail
    path('checkout/<int:pk>/', views.resend_mail, name='resend_mail'),
    #-- About us
    path('conocenos/', views.info, name='info'),
    #-- Contact
    path('contacto/', views.contact, name='contact'),
    #-- 404
    path('404/',TemplateView.as_view(template_name='404.html')),
]