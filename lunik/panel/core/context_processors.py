# -*- coding: utf-8 -*-
import json
from django.core.cache import cache
from django.urls import resolve
from django.apps import apps
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from decouple import config
from django.conf import settings
from django.shortcuts import get_object_or_404
from panel.config.models import PanelAdmin
from panel.config.models import ModuleItem
from panel.accounts.models import UserModulePermission, User, Role, UserModuleGroup,\
                                UserModulePermissionAction, UserModuleGroupAction

from portal.shop.cart import Cart
from panel.products.models import Product


#-- Data Panel on the CMS
def data_panel(request):
    context = {}

    #-- Get menu in cache
    panel = cache.get('datapanel_%s' % (config('REDIS_PREFIX')))

    if not panel:
        panel = PanelAdmin.objects.first()
        cache.set('datapanel_%s' % (config('REDIS_PREFIX')),panel)

    context['datapanel'] = panel

    return context

def module_name(request):
    context = {}

    ModuleItem = apps.get_model('config','ModuleItem')
    ModuleSubItem = apps.get_model('config','ModuleSubItem')

    func,args,kwargs = resolve(request.path)
    module = func.__module__

    module_name = module.split(".").pop()

    try:
        context['module'] = ModuleItem.objects.values('title').get(module=module_name)
    except ModuleItem.DoesNotExist:
        try:
            context['module'] = ModuleSubItem.objects.values('title').get(module=module_name)
        except ModuleSubItem.DoesNotExist:
            pass

    return context

#-- List of user´s modules
def menu_user(request,middle=None):
    context = {}

    if request.user.is_authenticated:
        #user = User.objects.get(pk=request.user.pk)

        #-- Get menu from cache
        menu = cache.get('menu_%s_%s' % (config('REDIS_PREFIX'),request.user.pk))

        if not menu:
            if request.user.is_superuser:
                menu = ModuleItem.objects.prefetch_related('subitems').filter(status=True,is_module=True,is_global=False)\
                                         .exclude(is_store=True).order_by('-order')
            else:
                if request.user.user_groups.exists():
                    menu = UserModuleGroup.objects.select_related('role','menu_item','menu_subitems')\
                                        .filter(role__user=request.user,menu_item__is_global=False)\
                                        .order_by('-menu_item__order','menu_item__title','menu_subitems__order')
                else:
                    menu = UserModulePermission.objects.filter(user=request.user,menu_item__is_global=False)\
                                                    .order_by('-menu_item__order','menu_item__title','menu_subitems__order')

            #-- Set menu in cache
            cache.set('menu_%s_%s' % (config('REDIS_PREFIX'),request.user.pk),menu)

        #-- Set menu list in context
        context['menu_user'] = menu

    if middle:
        return menu
    else:
        return context

#-- List of top user´s modules
def menu_top(request,middle=None):
    context = {}

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)

        #-- Get top menu in cache
        menu = cache.get('menu_top_%s_%s' % (config('REDIS_PREFIX'),request.user.pk))

        if not menu:
            if request.user.is_superuser:
                menu = ModuleItem.objects.prefetch_related('subitems').filter(status=True,is_module=True,is_global=True).order_by('order')
            else:
                if user.user_groups.exists():
                    menu = UserModuleGroup.objects.select_related('role','menu_item','menu_subitems')\
                                        .filter(role__user=request.user,menu_item__is_global=True).order_by('menu_item__order')
                else:
                    menu = UserModulePermission.objects.filter(user=request.user,menu_item__is_global=True).order_by('menu_item__order')
            cache.set('menu_top_%s_%s' % (config('REDIS_PREFIX'),request.user.pk),menu)

        context['menu_top'] = menu

    if middle:
        return menu
    else:
        return context

#-- List of module`s actions
def module_action(request):
    context = {}

    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)

        #-- Get actions from cache
        actions = cache.get('actions_%s_%s' % (config('REDIS_PREFIX'),request.user.pk))

        if not actions:
            if not request.user.is_superuser:
                if user.user_groups.exists():
                    actions = UserModuleGroupAction.objects.values('menu_item__module','menu_subitem__module',\
                                                                'can_add','can_edit','can_delete')\
                                                                .filter(role__user=request.user,menu_item__is_global=False)
                else:
                    actions = UserModulePermissionAction.objects.values('menu_item__module','menu_subitem__module',\
                                                                    'can_add','can_edit','can_delete')\
                                                                    .filter(user=request.user,menu_item__is_global=False)
            #-- Set actions in cache
            cache.set('actions_%s_%s' % (config('REDIS_PREFIX'),request.user.pk),actions)

        func,args,kwargs = resolve(request.path)
        module = func.__module__

        module_name = module.split(".").pop()

        if actions:
            for item in actions:
                if module_name == item['menu_item__module'] or module_name == item['menu_subitem__module']:
                    context['class_action_add'] = 'class_action_add' if not item['can_add'] else ''
                    context['class_action_edit'] = 'class_action_edit' if not item['can_edit'] else ''
                    context['class_action_delete'] = 'class_action_delete' if not item['can_delete'] else ''

    return context


def cart(request):

    return {'cart':Cart(request)}

def products_menu(request):
    context = {}
    context['products_list'] = Product.objects.prefetch_related('products_properties').filter(available=True, status=True).order_by('-created')

    return context

def pk_stripe(request):
    context = {}
    context['pk_stripe'] = settings.STRIPE_PUBLIC_KEY

    return context
