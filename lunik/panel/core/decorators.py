# -*- coding: utf-8 -*-
from django.db import connection, reset_queries
import time
import functools
import datetime
import requests
from decouple import config

from datetime import date
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import resolve
from django.shortcuts import get_object_or_404

from panel.accounts.models import User

#--- Request only if is Ajax
def ajax_required(f):
	def wrap(request, *args, **kwargs):
		if not request.is_ajax():
			return HttpResponseBadRequest()

		return f(request, *args, **kwargs)

	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__

	return wrap

#-- Method only for Superuser
def access_for_superuser(function):
    def wrap(request, *args, **kwargs):
        user = get_object_or_404(User,pk=request.user.pk)
        if user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect('authorization:login')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    wrap.__module__ = function.__module__

    return wrap

#-- Method only for User
def access_for_user(function):
    def wrap(request, *args, **kwargs):
        user = get_object_or_404(User,pk=request.user.pk)
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        elif request.user.is_superadmin:
            if not user.is_superuser:
                return function(request, *args, **kwargs)
        elif not user.is_superuser and not user.is_superadmin and not user.is_customer:
            return function(request, *args, **kwargs)

        return redirect('shop:shop_list')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    wrap.__module__ = function.__module__

    return wrap
def access_for_customer(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            user = get_object_or_404(User,pk=request.user.pk)
            if user.is_customer:
                return function(request, *args, **kwargs)
            return redirect('shop:shop_list')
        else:
            return redirect('register:login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    wrap.__module__ = function.__module__

    return wrap
def debugger_queries(func):
    """Basic function to debug queries."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("func: ", func.__name__)
        reset_queries()

        start = time.time()
        start_queries = len(connection.queries)

        result = func(*args, **kwargs)

        end = time.time()
        end_queries = len(connection.queries)

        print("queries:", end_queries - start_queries)
        print("took: %.2fs" % (end - start))
        return result

    return wrapper

#-- Google ReCaptcha
def check_recaptcha(function):
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')

            data = {
                'secret': config('GOOGLE_RECAPTCHA_SECRET_KEY'),
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False

        return function(request, *args, **kwargs)

    return wrap
