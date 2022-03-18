# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
	#-- List Panel Data
    path('data/', views.panel_list, name='panel_list'),
	#-- Add Panel Data
    path('data/add/', views.panel_add, name='panel_add'),
	#-- Edit Panel Data
    path('data/edit/<int:pk>/', views.panel_edit, name='panel_edit'),

	#-- List Menu Items
    path('menu/', views.menu_list, name='menu_list'),
	#-- Add Menu Item
    path('menu/add/', views.menu_add, name='menu_add'),
	#-- Edit Menu Item
    path('menu/edit/<int:pk>/', views.menu_edit, name='menu_edit'),
    #-- Delete Menu Item
    path('menu/delete/<int:pk>/', views.menu_delete, name='menu_delete'),

	#-- List SubMenu Items
    path('submenu/', views.submenu_list, name='submenu_list'),
	#-- Add SubMenu Item
    path('submenu/add/', views.submenu_add, name='submenu_add'),
	#-- Edit SubMenu Item
    path('submenu/edit/<int:pk>/', views.submenu_edit, name='submenu_edit'),
    #-- Delete SubMenu Item
    path('submenu/delete/<int:pk>/', views.submenu_delete, name='submenu_delete'),
	#-- List components
    path('templates/components/', views.component_list, name='component_list'),
	#-- Add component Item
    path('templates/components/add/', views.component_add, name='component_add'),
	#-- Edit component Item
    path('templates/components/<int:pk>/', views.component_edit, name='component_edit'),
    #-- Delete component Item
    path('templates/components/<int:pk>/', views.component_delete, name='component_delete'),
    path('templates/component/<int:pk>/', views.component, name='component'),
	#-- List Sessions
    path('account/sessions/', views.sessions_list, name='sessions_list'),
    path('account/sessions/<int:pk>/delete/', views.sessions_delete, name='sessions_delete'),
]
