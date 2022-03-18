# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	#-- Dashboard
	path('', views.dashboard, name='dashboard'),
	#-- Login
    path('login/', views.login_account, name='login'),
    #-- Logout
    path('logout/', views.logout_account, name='logout'),
    #-- Recover Store
    path('recovery/store/', views.recover_store, name='recover_store'),

]
