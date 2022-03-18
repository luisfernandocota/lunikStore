# -- production.py
from .common import *

DEBUG = config('DEBUG',default=False,cast=bool)

#-- Errors 404
SEND_BROKEN_LINK_EMAILS = True

ALLOWED_HOSTS = config('DOMAIN_NAME',default='127.0.0.1',cast=Csv())

#-- HTTPS SERVER DOMAIN
if config('IS_SECURE',default=False,cast=bool):
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_DOMAIN = config('DOMAIN_NAME')
    CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

    SESSION_COOKIE_SECURE = True