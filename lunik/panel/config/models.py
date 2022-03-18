# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import datetime

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

def get_filename(extension):
	ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	return '%s%s' % (ts, extension)

def get_logo(instance, filename):
    name, ext = os.path.splitext(filename)

    return 'paneladmin/%s' % get_filename(ext)

# Create your models here.
class PanelAdmin(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    url = models.URLField(max_length=200, verbose_name='URL', blank=True)
    logo = models.ImageField(upload_to=get_logo, verbose_name='Logo Login')
    author = models.CharField(max_length=100, verbose_name='Autor')

    class Meta:
        db_table = 'panel_admin'
        verbose_name = 'Dato'
        verbose_name_plural = 'Datos'

    def __str__(self):
        return self.title

class Logger(TimeStampedModel):
    LOG_INFO = 'I'
    LOG_ACCESS = 'A'
    LOG_ERROR = 'E'
    LOGS_TYPE = (
        (LOG_INFO, 'Info'),
        (LOG_ACCESS, 'Acceso'),
        (LOG_ERROR, 'Error'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='logger',verbose_name='Usuario',on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='IPv4',verbose_name='IP')
    sessionkey = models.CharField(max_length=40,verbose_name='Sesión',blank=True)
    logtype = models.CharField(max_length=1,choices=LOGS_TYPE,verbose_name='Tipo de Log')
    user_agent = models.CharField(max_length=250,verbose_name='Navegador',blank=True)
    message = models.CharField(max_length=200,verbose_name='Mensaje',blank=True)
    url = models.URLField(verbose_name='URL')

    class Meta:
        db_table = 'users_logs'
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ('-created',)

    def __str__(self):
        return self.user.get_full_name

class ModuleItem(models.Model):
    app_label = models.CharField(max_length=80,verbose_name='App Label')
    title = models.CharField(max_length=120, verbose_name='Título')
    module = models.CharField(max_length=120, verbose_name='Módulo',blank=True)
    url = models.CharField(max_length=120,verbose_name='URL')
    icon = models.CharField(max_length=60, verbose_name='icono')
    order = models.PositiveSmallIntegerField(verbose_name='Orden',default=0)
    has_submenu = models.BooleanField(verbose_name='Con Submenu',default=False)
    is_menu = models.BooleanField(verbose_name='Es Menú',default=True)
    is_module = models.BooleanField(verbose_name='Es Módulo',default=True)
    is_global = models.BooleanField(verbose_name='Es Global',default=False)
    is_store = models.BooleanField(verbose_name='Es Tienda',default=False)
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'modules_items'
        verbose_name = 'Módulos'
        verbose_name_plural = 'Módulos'
        ordering = ('order',)

    def __str__(self):
        return self.title

    def subitems_list(self):
        return self.subitems.filter(status=True)

class ModuleSubItem(models.Model):
    item = models.ForeignKey(ModuleItem, related_name='subitems',on_delete=models.CASCADE, verbose_name='Item')
    title = models.CharField(max_length=120, verbose_name='Título')
    module = models.CharField(max_length=120, verbose_name='Módulo',default='')
    url = models.CharField(max_length=120,verbose_name='URL')
    icon = models.CharField(max_length=60, verbose_name='icono',blank=True)
    order = models.PositiveSmallIntegerField(verbose_name='Orden',default=0)
    is_submenu = models.BooleanField(verbose_name='Es Submódulo',default=True)
    is_store = models.BooleanField(verbose_name='Es Tienda',default=False)		
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'modules_subitems'
        verbose_name = 'Sub Módulos'
        verbose_name_plural = 'Sub Módulos'
        ordering = ('order',)

    def __str__(self):
        return self.title

class TemplateComponent(models.Model):
    name = models.CharField(max_length=120, verbose_name='Name')
    code = models.TextField(verbose_name='Codigo')
    status = models.BooleanField(default=True, verbose_name='Status')

    class Meta:
        db_table = 'template_components'
        verbose_name_plural = 'Componentes'
