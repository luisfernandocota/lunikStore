# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models

from django_extensions.db.models import TimeStampedModel

from panel.core.utils import get_filename


def get_slide(instance, filename):
    name, ext = os.path.splitext(filename)

    return 'slide/%s' % (get_filename(ext))

class Slide(TimeStampedModel):
    title = models.CharField(max_length=120,verbose_name='Título', null=True, blank=True)
    url = models.URLField(verbose_name='URL',blank=True, null=True)
    image = models.ImageField(verbose_name='Imagen',upload_to=get_slide)
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'slides'
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'

    def __str__(self):
        return self.title


# class New(TimeStampedModel):
#     title = models.CharField(max_length=200, verbose_name='Título')
#     slug = models.SlugField(max_length=200, unique=True, verbose_name='Enlace (Personalizado)')
#     image = models.ImageField(upload_to=get_image_cover, verbose_name='Foto Principal')
#     description = models.CharField(max_length=350, verbose_name='Descripción')
#     detail = models.TextField(verbose_name='Detalle')
#     file_name = models.CharField(max_length=200, verbose_name='Nombre del archivo')
#     url = models.URLField(blank=True, null=True)
#     status = models.BooleanField(verbose_name='Activo', default=True)

#     class Meta:
#         db_table = 'news'
#         ordering = ['-created', 'title']
#         verbose_name = 'Noticia'
#         verbose_name_plural = 'Noticias'

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('news_site:news_detail', kwargs={'slug': self.slug})

#     @property
#     def get_full_url(self):
#         current_site = Site.objects.get_current()
#         return '{}{}'.format(current_site.domain, self.get_absolute_url())

#     @property
#     def get_img_full_url(self):
#         if self.image:
#             current_site = Site.objects.get_current()
#             return '{}{}'.format(current_site.domain, self.image.url)
#         else:
#             return ''

#     def save(self, *args, **kwargs):
#         #-- slug title
#         self.slug = slugify(self.title)

#         super(New, self).save(*args, **kwargs)

# class NewGallery(TimeStampedModel):
#     new = models.ForeignKey(New, related_name='gallery', verbose_name='Noticia', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=get_image_gallery, verbose_name='Imagen', blank=True)
#     footer = models.CharField(max_length=200, verbose_name='Pie de Página', blank=True)

#     class Meta:
#         db_table = 'news_gallery'
#         ordering = ['id']
#         verbose_name = 'Imagen'
#         verbose_name_plural = 'Galeria'

# post_delete.connect(file_cleanup, sender=NewGallery)
# Create your models here.
class Faq(TimeStampedModel):
    question = models.CharField(max_length=200,verbose_name='Question')
    answer = models.TextField(verbose_name='Answer')
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'faqs'
        verbose_name = 'Faq'
        verbose_name_plural = 'Faqs'

    def __str__(self):
        return self.question

# class ActivityDesign(models.Model):
#     name = models.CharField(max_length=200,verbose_name='Name')
#     image = models.ImageField(verbose_name='Diseño',upload_to=get_activity_design)
#     status = models.BooleanField(verbose_name='Status',default=True)

#     class Meta:
#         db_table = 'activities_designs'
#         verbose_name = 'Activity'
#         verbose_name_plural = 'Activities'

#     def __str__(self):
#         return self.name

# class ActivityDesignGallery(models.Model):
#     activity = models.ForeignKey(ActivityDesign, related_name='activities_gallery', verbose_name='Activity', on_delete=models.CASCADE)
#     image = models.FileField(upload_to=get_activity_design_gallery, validators=[validate_file_extension],verbose_name='Image')

#     class Meta:
#         db_table = 'activities_designs_gallery'
#         ordering = ['id']
#         verbose_name = 'Gallery'
#         verbose_name_plural = 'Gallery'

# class Banner(models.Model):
#     store_meta = models.OneToOneField(StoreMeta, related_name="banners", on_delete=models.CASCADE)
#     banner_about = models.ImageField(upload_to=get_banner_a, verbose_name="Banner about us", null=True, blank=True)
#     banner_contact = models.ImageField(upload_to=get_banner_c, verbose_name="Banner contact", blank=True, null=True)
#     banner_checkout = models.ImageField(upload_to=get_banner_ch, verbose_name="Banner checkout", blank=True, null=True)
#     banner_success = models.ImageField(upload_to=get_banner_s, verbose_name="Banner success", blank=True, null=True)
#     banner_error = models.ImageField(upload_to=get_banner_e, verbose_name="Banner error", blank=True, null=True)

#     class Meta:
#         db_table = 'store_banners'
#         ordering = ['id']
#         verbose_name = 'Banner'
#         verbose_name_plural = 'Banners'

# class Info(models.Model):
#     store_meta = models.OneToOneField(StoreMeta, related_name="info", on_delete=models.CASCADE)
#     email_store = models.EmailField(max_length=80, verbose_name='Correo de la tienda', null=True, blank=True)
#     phone_store = models.CharField(max_length=30, verbose_name='Télefono de la tienda', null=True, blank=True)
#     txt_header = models.CharField(max_length=150, verbose_name='Text Header', default='Ingresa el texto que quieras aqui')
#     detail = models.TextField(verbose_name='Detalle', null=True)
#     has_video = models.BooleanField(verbose_name='Has video?', default=False)
#     url_video = models.URLField(verbose_name='Video URL', null=True, help_text='https://www.youtube.com/embed/ScMzIvxBSi4')
#     image_video = models.ImageField(upload_to=get_image_video, verbose_name='Imagen del video', null=True, blank=True)
#     facebook = models.CharField(max_length=120, verbose_name='Facebook', null=True, help_text='Nombre de usuario')
#     pixel = models.TextField(verbose_name='Facebook Pixel', null=True)
#     messenger = models.TextField(verbose_name='Facebook messenger', null=True)
#     same_email = models.BooleanField(default=False, verbose_name='Same Email?')
#     same_wapp = models.BooleanField(default=False, verbose_name='Same Whatsapp?')
#     whatsapp = models.CharField(max_length=30, verbose_name='Whatsapp', null=True, blank=True)
#     instagram = models.CharField(max_length=120, verbose_name='Instagram', null=True, help_text='Nombre de usuario')
#     pinterest = models.CharField(max_length=120, verbose_name='Pinterest', null=True, help_text='Nombre de usuario')
#     youtube = models.CharField(max_length=120, verbose_name='Youtube', null=True, help_text='Nombre de usuario')
#     snapchat = models.CharField(max_length=120, verbose_name='Snapchat', null=True, help_text='Nombre de usuario')
#     has_address = models.BooleanField(default=False, verbose_name='Has address?')

#     class Meta:
#         db_table = 'info'
#         verbose_name = 'Information'

#     def __str__(self):
#         return self.txt_header

# class Office(models.Model):
#     store_meta = models.OneToOneField(StoreMeta, related_name="office", on_delete=models.CASCADE)
#     name = models.CharField(max_length=130, verbose_name='Name', null=True)
#     address =  models.CharField(max_length=100, verbose_name='Address', null=True)
#     phone = models.CharField(max_length=30, verbose_name='Télefono', null=True, blank=True)
#     state = models.CharField(max_length=60, verbose_name='State', null=True)
#     city = models.CharField(max_length=60, verbose_name='city', null=True)
#     status = models.BooleanField(verbose_name='Activo', default=True)
#     latitude = models.CharField(max_length=150,verbose_name='Latitud', null=True)
#     longitude = models.CharField(max_length=150,verbose_name='Longitud', null=True)
#     class Meta:
#         db_table = 'office'
#         verbose_name = 'Office'

#     def __str__(self):
#         return self.name