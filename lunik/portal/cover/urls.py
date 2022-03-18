# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	#-- Cover
    path('', views.index, name='index'),
]
