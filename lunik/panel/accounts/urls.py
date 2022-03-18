# -*- coding: utf-8 -*-

from django.urls import path,re_path
from . import views

urlpatterns = [
	#-- List Users
    path('', views.accounts_list, name='accounts_list'),
	#-- Add User
    path('add/', views.accounts_add, name='accounts_add'),
	#-- Edit User
    path('edit/<int:pk>/', views.accounts_edit, name='accounts_edit'),
    #-- Delete User
    path('delete/<int:pk>/', views.accounts_delete, name='accounts_delete'),
    #-- Mail Activation User
    path('sendmail_activation/<int:pk>/', views.accounts_sendmail_activation, name='accounts_sendmail_activation'),
    #-- Mail Activation User
    path('resend_mail/<int:customer_pk>/', views.resend_mail, name='resend_mail'),
    #-- Activation Link User
    re_path(r'^activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.accounts_activation, name='accounts_activation'),
    #-- Logs List
    path('logs/<int:pk>/', views.accounts_logs, name='accounts_logs'),
	#-- User Role Ajax
    path('role/', views.accounts_role, name='accounts_role'),
	#-- User Permissions list
    path('permissions_list/', views.accounts_permissions_list, name='accounts_permissions_list'),

	#-- List User Roles
    path('roles/', views.roles_list, name='roles_list'),
	#-- Add User Role
    path('roles/add/', views.roles_add, name='roles_add'),
	#-- Edit User Role
    path('roles/edit/<int:pk>/', views.roles_edit, name='roles_edit'),
    #-- Delete User Role
    path('roles/delete/<int:pk>/', views.roles_delete, name='roles_delete'),

	#-- List User Group
    path('usergroups/', views.usergroups_list, name='usergroups_list'),
	#-- Add User Group
    path('usergroups/add/', views.usergroups_add, name='usergroups_add'),
	#-- Edit User Group
    path('usergroups/edit/<int:pk>/', views.usergroups_edit, name='usergroups_edit'),
    #-- Delete User Groups
    path('usergroups/delete/<int:pk>/', views.usergroups_delete, name='usergroups_delete'),
]
