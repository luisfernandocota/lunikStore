# -- production.py
from .common import *

DEBUG = config('DEBUG',default=False,cast=bool)

#-- Errors 404
SEND_BROKEN_LINK_EMAILS = True

ALLOWED_HOSTS = config('DOMAIN_NAME',default='127.0.0.1',cast=Csv())

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

#COMPRESS_ROOT = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

#COMPRESS_ENABLED = True
#COMPRESS_OFFLINE = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

#-- HTTPS SERVER DOMAIN
if config('IS_SECURE',default=False,cast=bool):
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_DOMAIN = config('DOMAIN_NAME')
    CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

    SESSION_COOKIE_SECURE = True