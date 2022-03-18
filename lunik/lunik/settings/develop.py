# -- develop.py
from .common import *

DEBUG = config('DEBUG',default=True,cast=bool)
ALLOWED_HOSTS = ['*']