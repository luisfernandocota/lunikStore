# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    #-- Faqs list
    path('faqs/', views.faqs_list, name='faqs_list'),
    #-- Faqs add
    path('faqs/add/', views.faqs_add, name='faqs_add'),
    #-- Faqs edit
    path('faqs/edit/<int:pk>/', views.faqs_edit, name='faqs_edit'),
    #-- Faqs delete
    path('faqs/delete/<int:pk>/', views.faqs_delete, name='faqs_delete'),

    #-- Slide list
    path('slides/', views.slides_list, name='slides_list'),
    #-- Slide add
    path('slides/add/', views.slides_add, name='slides_add'),
    #-- Slide edit
    path('slides/edit/<int:pk>/', views.slides_edit, name='slides_edit'),
    #-- Slide delete
    path('slides/delete/<int:pk>/', views.slides_delete, name='slides_delete'),


    path('customers/', views.customers_list, name='customers_list')
 
]
