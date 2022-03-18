# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime

from datetime import date
from django.db import models
from django.conf import settings
from django.apps import apps
from django.urls import reverse
from django.db.models.signals import post_delete
from django.template.loader import render_to_string
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django_extensions.db.models import TimeStampedModel
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.crypto import get_random_string
from django.core.cache import cache

from panel.core.tokens import account_activation_token
from panel.core.managers import UserManager
from panel.core.signals import file_cleanup
from panel.core.utils import get_filename,sendmail
from panel.core.validators import validate_file_extension
from panel.config.models import ModuleItem, ModuleSubItem

def get_avatar(instance, filename):
    name, ext = os.path.splitext(filename)

    return 'accounts/%s' % get_filename(ext)

class Role(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='user_groups',verbose_name='Usuario')
    name = models.CharField(max_length=80, verbose_name='Nombre')
    description = models.CharField(max_length=120, verbose_name='Descripción', blank=True)
    is_group = models.BooleanField(verbose_name='Es grupo', default=False)
    status = models.BooleanField(verbose_name='Status', default=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE,'Masculino'),
        (FEMALE,'Femenino'),
    )
    email = models.EmailField(max_length=120, verbose_name='Email', unique=True)
    first_name = models.CharField(max_length=120, verbose_name='Nombre')
    last_name = models.CharField(max_length=120, verbose_name='Apellidos')
    phone = models.CharField(max_length=30, verbose_name='Teléfono', blank=True)
    gender = models.CharField(max_length=2, choices=GENDER, verbose_name='Gender', null=True, blank=True)
    birthday = models.DateField(verbose_name="Birth Day", null=True, blank=True)
    avatar = models.ImageField(upload_to=get_avatar,validators=[validate_file_extension],verbose_name='Avatar', blank=True)
    facebook = models.CharField(max_length=120, verbose_name='Facebook', blank=True, help_text='Nombre de usuario')
    twitter = models.CharField(max_length=120, verbose_name='Twitter', blank=True, help_text='@su_nick')
    role = models.ForeignKey(Role, related_name='users', verbose_name='Rol de Usuario', null=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Activo', default=False)
    is_superadmin = models.BooleanField(verbose_name='Superadmin', default=False)
    is_customer = models.BooleanField(verbose_name='Es cliente?', default=False)
    is_client = models.BooleanField(verbose_name='Es cliente 4shop?', default=False)
    status = models.BooleanField(verbose_name='Status', default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        ordering = ['email']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('profile:profile_edit')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @staticmethod
    def activation_email(request,user,password, own_password=False):

        #-- Send email
        #-- Get menu in cache
        has_password = own_password
        panel = cache.get('datapanel')
        if not panel:
            PanelAdmin = apps.get_model('config','PanelAdmin')
            panel = PanelAdmin.objects.first()

            cache.set('datapanel',panel)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        subject = 'Lunik :: ACTIVACIÓN DE CUENTA'
        message = render_to_string('accounts/accounts_email.html', {
                                    'email': user.email,
                                    'password': password,
                                    'request': request,
                                    'uid': uid.encode().decode(),
                                    'token': token,
                                        'own_password': has_password,
                                        'reseller': True,
                                    })

        expires_key = datetime.datetime.today() + datetime.timedelta(2)
        #-- Save activation token
        user_activation = UserRequest.objects.create(user=user, uid=uid, token=token, expires_key=expires_key)

        sendmail(subject, message, settings.DEFAULT_FROM_EMAIL, user.email)

        return user_activation

    @staticmethod
    def activation_url(uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            user_activation = UserRequest.objects.filter(token=token).first()
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token) and user_activation.activation_status == '0':
            user.is_active = True
            user.save()
            user_activation.activation_status = '1'
            user_activation.save()

            return user
        else:
            return False

    @staticmethod
    def create_account_group(request,role,form):
        group = Role.objects.get(name=role)
        #-- Create User
        user = User(email=form.cleaned_data['email'],first_name=form.cleaned_data['first_name']\
                    ,last_name=form.cleaned_data['last_name'],role=group)
        user.save()

        #-- Generate random password
        password = get_random_string(10)
        user.set_password(password)
        user.save()

        #-- Send activation email
        User.activation_email(request,user,password)

        #-- Save relation User/ Group
        group.user.add(user)

        #-- Return User
        return user

    @staticmethod
    def modules_list():
        return ModuleItem.objects.prefetch_related('subitems').filter(status=True,is_module=True).order_by('order')

    @staticmethod
    def save_modules_list(modules_list,user, change):
        #-- Edit User
        if change:
            UserModulePermission.objects.filter(user=user).delete()

        for item in modules_list:
            module = item.split('|')
            if module[1] == '1':
                submenu = ModuleSubItem.objects.get(pk=module[0])
                UserModulePermission.objects.create(user=user,menu_item=submenu.item,menu_subitems=submenu)
            else:
                menu = ModuleItem.objects.get(pk=module[0])
                UserModulePermission.objects.create(user=user,menu_item=menu)

    @staticmethod
    def save_modules_group(modules_list, form, change):
        #-- Edit Group
        if change:
            UserModuleGroup.objects.filter(role=form.cleaned_data['role']).delete()

        for item in modules_list:
            module = item.split('|')
            if module[1] == '1':
                submenu = ModuleSubItem.objects.get(pk=module[0])
                UserModuleGroup.objects.create(role=form.cleaned_data['role'],menu_item=submenu.item,menu_subitems=submenu)
            else:
                menu = ModuleItem.objects.get(pk=module[0])
                UserModuleGroup.objects.create(role=form.cleaned_data['role'],menu_item=menu)

    @staticmethod
    def delete_modules_user(item):
        UserModulePermission.objects.filter(menu_item=item).delete()

    @staticmethod
    def delete_submodules_user(item):
        UserModulePermission.objects.filter(menu_subitems=item).delete()


post_delete.connect(file_cleanup,sender=User)

class UserRequest(models.Model):
    ACTIVATIONSTATUS_CHOICES = (
        (0, 'Enviado'),
        (1, 'Activado o Expirado'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activation', on_delete=models.CASCADE)
    uid = models.CharField(max_length=20, default='')
    token = models.CharField(max_length=60, default='')
    expires_key = models.DateTimeField(default=datetime.datetime.now)
    activation_status = models.CharField(max_length=2, choices=ACTIVATIONSTATUS_CHOICES, default='0')
    activation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_requests'

class UserModulePermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_permisssion', verbose_name='Usuario',on_delete=models.CASCADE)
    menu_item = models.ForeignKey(ModuleItem, related_name='user_items',verbose_name='Items',on_delete=models.CASCADE)
    menu_subitems = models.ForeignKey(ModuleSubItem, related_name='user_subitems',verbose_name='SubItems',null=True,on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'users_modules_permissions'
        verbose_name = 'Permisos de usuarios'

    def __str__(self):
        return self.user.get_full_name()

class UserModuleGroup(models.Model):
    role = models.ForeignKey(Role, related_name='group', verbose_name='Rol de usuario',on_delete=models.CASCADE)
    menu_item = models.ForeignKey(ModuleItem, related_name='group_items',verbose_name='Items',on_delete=models.CASCADE)
    menu_subitems = models.ForeignKey(ModuleSubItem, related_name='group_subitems',verbose_name='SubItems',null=True,on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'groups_modules_permissions'
        verbose_name = 'Permisos de grupo'

    def __str__(self):
        return self.role.name

class UserModulePermissionAction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_permisssion_actions', verbose_name='Usuario',on_delete=models.CASCADE)
    menu_item = models.ForeignKey(ModuleItem, related_name='actions_items',verbose_name='Items',on_delete=models.CASCADE)
    menu_subitem = models.ForeignKey(ModuleSubItem, related_name='actions_subitems',verbose_name='SubItems',null=True,on_delete=models.CASCADE)
    can_add = models.BooleanField(verbose_name='Agregar',default=False)
    can_edit = models.BooleanField(verbose_name='Modificar',default=False)
    can_delete = models.BooleanField(verbose_name='Eliminar',default=False)

    class Meta:
        db_table = 'users_modules_actions'
        verbose_name = 'Acciones sobre módulos'

    def __str__(self):
        return self.user.get_full_name()

class UserModuleGroupAction(models.Model):
    role = models.ForeignKey(Role, related_name='group_actions', verbose_name='Rol de usuario',on_delete=models.CASCADE)
    menu_item = models.ForeignKey(ModuleItem, related_name='actions_group_items',verbose_name='Items',on_delete=models.CASCADE)
    menu_subitem = models.ForeignKey(ModuleSubItem, related_name='actions_group_subitems',verbose_name='SubItems',null=True,on_delete=models.CASCADE)
    can_add = models.BooleanField(verbose_name='Agregar',default=True)
    can_edit = models.BooleanField(verbose_name='Modificar',default=True)
    can_delete = models.BooleanField(verbose_name='Eliminar',default=True)

    class Meta:
        db_table = 'groups_modules_actions'
        verbose_name = 'Acciones sobre permisos de grupos'

    def __str__(self):
        return self.role.name
