# Generated by Django 2.2.4 on 2021-08-05 05:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import panel.accounts.models
import panel.core.managers
import panel.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('email', models.EmailField(max_length=120, verbose_name='Email')),
                ('first_name', models.CharField(max_length=120, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=120, verbose_name='Apellidos')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Teléfono')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=2, null=True, verbose_name='Gender')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birth Day')),
                ('avatar', models.ImageField(blank=True, upload_to=panel.accounts.models.get_avatar, validators=[panel.core.validators.validate_file_extension], verbose_name='Avatar')),
                ('facebook', models.CharField(blank=True, help_text='Nombre de usuario', max_length=120, verbose_name='Facebook')),
                ('twitter', models.CharField(blank=True, help_text='@su_nick', max_length=120, verbose_name='Twitter')),
                ('is_active', models.BooleanField(default=False, verbose_name='Activo')),
                ('is_superadmin', models.BooleanField(default=False, verbose_name='Superadmin')),
                ('is_customer', models.BooleanField(default=False, verbose_name='Es cliente?')),
                ('is_client', models.BooleanField(default=False, verbose_name='Es cliente 4shop?')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'users',
                'ordering': ['email'],
            },
            managers=[
                ('objects', panel.core.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=120, verbose_name='Descripción')),
                ('is_group', models.BooleanField(default=False, verbose_name='Es grupo')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='UserModuleGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Permisos de grupo',
                'db_table': 'groups_modules_permissions',
            },
        ),
        migrations.CreateModel(
            name='UserModuleGroupAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_add', models.BooleanField(default=True, verbose_name='Agregar')),
                ('can_edit', models.BooleanField(default=True, verbose_name='Modificar')),
                ('can_delete', models.BooleanField(default=True, verbose_name='Eliminar')),
            ],
            options={
                'verbose_name': 'Acciones sobre permisos de grupos',
                'db_table': 'groups_modules_actions',
            },
        ),
        migrations.CreateModel(
            name='UserModulePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Permisos de usuarios',
                'db_table': 'users_modules_permissions',
            },
        ),
        migrations.CreateModel(
            name='UserModulePermissionAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_add', models.BooleanField(default=False, verbose_name='Agregar')),
                ('can_edit', models.BooleanField(default=False, verbose_name='Modificar')),
                ('can_delete', models.BooleanField(default=False, verbose_name='Eliminar')),
            ],
            options={
                'verbose_name': 'Acciones sobre módulos',
                'db_table': 'users_modules_actions',
            },
        ),
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='', max_length=20)),
                ('token', models.CharField(default='', max_length=60)),
                ('expires_key', models.DateTimeField(default=datetime.datetime.now)),
                ('activation_status', models.CharField(choices=[(0, 'Enviado'), (1, 'Activado o Expirado')], default='0', max_length=2)),
                ('activation_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_requests',
            },
        ),
    ]
