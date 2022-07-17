# -- develop.py
from .common import *

DEBUG = config('DEBUG',default=True,cast=bool)
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
COMPRESS_ROOT = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)