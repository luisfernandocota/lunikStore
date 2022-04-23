# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views

urlpatterns = [
	#-- Profile
	path('perfil/', views.profile, name='profile'),
	#-- Edit profile
	path('editar_perfil/', views.edit_profile, name='edit_profile'),
	#-- List Address
	path('direcciones/', views.address, name='address'),
	path('direcciones/agregar/', views.add_address, name='add_address'),
	path('direcciones/editar/<int:pk>', views.edit_address, name='edit_address'),
	path('zipcode/info/', views.get_zip_code, name='zipcode'),
	#-- Orders
	path('ordenes/', views.orders, name="orders"),
	#-- Get Order detail
	path('ordenes/detalle/<int:pk>', views.order_detail, name='order_detail'),

	#-- Cancel order
	path('orden/cancelar/<int:pk>', views.order_cancel, name='order_cancel'),
	#-- Change password
    path('cambiar_contrasena/', views.password_edit, name='password_edit'),
]