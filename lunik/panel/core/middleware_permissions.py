#-- Author: Hugo Camargo <ratedchr@gmail.com>
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect,HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.urls import resolve
from re import compile

from decouple import config

from panel.config.models import ModuleItem, ModuleSubItem
from panel.core.context_processors import menu_user, menu_top

#from django.contrib.auth import get_user_model
#django.contrib.auth.models.User.get_full_name()

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class CheckPermissionsMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.user.is_authenticated and not request.user.is_anonymous:
            path = request.path_info.lstrip('/')

            func,args,kwargs = resolve(request.path)
            module = func.__module__

            module_name = module.split(".").pop()

            if not request.user.is_superuser:
                if not any(m.match(path) for m in EXEMPT_URLS):
                    menu = cache.get('menu_%s_%s' % (config('REDIS_PREFIX'),request.user.pk))
                    menut = cache.get('menu_top_%s_%s' % (config('REDIS_PREFIX'),request.user.pk))

                    if not menu:
                        menu = menu_user(request,True)
                    if not menut:
                        menut = menu_top(request,True)

                    if path != 'panel/' and path != 'panel/logout/' and path != 'panel/profile/' and path != 'panel/profile/change_password/':
                        has_perms = False

                        #-- Check if module is True
                        module_access = True
                        try:
                            module_obj = ModuleItem.objects.get(module=module_name)
                            if not module_obj.is_module:
                                module_access = False
                        except ModuleItem.DoesNotExist:
                             pass

                        if module_access:
                            for item in menu:
                                if module_name == item.menu_item.module:
                                    has_perms = True
                                elif item.menu_subitems is not None:
                                    if module_name == item.menu_subitems.module:
                                        has_perms = True

                            for item in menut:
                                if module_name == item.menu_item.module:
                                    has_perms = True
                                elif item.menu_subitems is not None:
                                    if module_name == item.menu_subitems.module:
                                        has_perms = True

                            #-- Has not permission to the module
                            if not has_perms:
                                raise PermissionDenied
