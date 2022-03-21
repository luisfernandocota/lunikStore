# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views

urlpatterns = [
	#-- Register
	path('registro/', views.register_user, name='add'),
	#-- Register Done
    path('hecho/<int:pk>/', views.register_done, name='done'),
    path('ingresar/', views.register_login, name='login'),
    path('cerrar/', views.register_logout, name='logout'),
    #-- Activation User
    re_path(r'^activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', \
         views.register_activation, name='register_activation'),
]