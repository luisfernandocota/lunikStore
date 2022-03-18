
from __future__ import unicode_literals

import os
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.utils.text import slugify
from panel.core.utils import get_filename,user_logs
from panel.core.validators import validate_file_extension

def get_logo(instance,filename):
    name, ext = os.path.splitext(filename)

    return 'products/brands/%s' % get_filename(ext)

def get_product_gallery(instance, filename):
	name, ext = os.path.splitext(filename)

	return 'products/gallery/%s' % (get_filename(ext))
# Create your models here.

class ProductSize(models.Model):
    name = models.CharField(max_length=35,verbose_name='Size')
    charge = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Cargo',null=True,blank=True)
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'sizes'
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.name

    def natural_key(self):
        return '%s-%s' % (self.name,self.charge)

class ProductHexaCode(models.Model):
    name = models.CharField(max_length=120,verbose_name='Name',default='')
    hexacode = models.CharField(max_length=7,verbose_name='Code')
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'hexacodes'
        verbose_name = 'Hexacode'
        verbose_name_plural = 'Hexacodes'

    def __str__(self):
        return self.hexacode

    def natural_key(self):
        return '%s - %s' %(self.name,self.hexacode)

class Product(TimeStampedModel):
    slug = models.SlugField(max_length=120, verbose_name='Slug',default=None)
    #brand = models.ForeignKey(ProductBrand,related_name='products',verbose_name='Brand', on_delete=models.CASCADE)
    brand = models.CharField(max_length=30,verbose_name='Brand')
    model = models.CharField(max_length=30,verbose_name='Model')
    name = models.CharField(max_length=120,verbose_name='Name')
    description  = models.TextField(verbose_name='Description')
    aditional = models.TextField(verbose_name='Info Aditional',null=True,blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price',null=True,blank=True)
    sizes = models.ManyToManyField(ProductSize,related_name='products_sizes')
    hexacodes = models.ManyToManyField(ProductHexaCode,related_name='products_hexacode',through='ProductHexaCodeM2M')
    available = models.BooleanField(verbose_name='Available',default=True)
    status = models.BooleanField(verbose_name='Status',default=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)

        super(Product,self).save(*args,**kwargs)

class ProductGallery(TimeStampedModel):
	product = models.ForeignKey(Product, related_name='products_gallery', verbose_name='Product', on_delete=models.CASCADE)
	image = models.FileField(upload_to=get_product_gallery, validators=[validate_file_extension],verbose_name='Image')

	class Meta:
		db_table = 'products_gallery'
		ordering = ['id']
		verbose_name = 'Gallery'
		verbose_name_plural = 'Gallery'

class ProductHexaCodeM2M(models.Model):
    product = models.ForeignKey(Product,related_name='hexacodes_m2m',on_delete=models.CASCADE)
    hexacode = models.ForeignKey(ProductHexaCode,on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Status',default=True)

    def __str__(self):
        return self.hexacode.hexacode

class ProductProperty(models.Model):
    product = models.OneToOneField(Product,related_name='products_properties', on_delete=models.CASCADE)
    sell_price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Sell Price', null=True, default=0)
    margin = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Margin', null=True, default=0)
    gain = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Gain', null=True, default=0)
    sale_price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Sale Price', null=True, default=0)
    is_sale = models.BooleanField(verbose_name='Sale', default=False)
    is_outstanding = models.BooleanField(verbose_name='Outstanding', default=False)
    shipping_price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Shipping to home', null=True, default=0)
    shipping_free = models.BooleanField(verbose_name='Shipping Free', default=False)
    shipping_min = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='Shipping min', null=True, default=0)
    has_personalization = models.BooleanField(verbose_name='Has_personalization',default=False)

    class Meta:
        db_table = 'product_properties'
        verbose_name_plural = 'Product properties'

    def __str__(self):
        return self.product.name

    def products_color(self):
        return self.products.all().select_related('hexacode').order_by('hexacode')

    def products_gallery(self):
        return self.products.products_gallery.filter(status=True).select_related('product')

class Coupon(TimeStampedModel):
    Select = 'S'
    Percentage = 'P'
    Amount = 'A'
    # BuyXGetY = 'B'
    DISCOUNT_TYPES = (
        (Select, 'Seleccione'),
        (Percentage, '% - Porcentaje'),
        (Amount, '$ - Monto'),
        # (BuyXGetY, 'Compra X, obtén Y')
    )
    code = models.CharField(max_length=30, verbose_name='Código')
    discount = models.PositiveSmallIntegerField(verbose_name='Descuento')
    discount_types = models.CharField(max_length=1,choices=DISCOUNT_TYPES,default='P',verbose_name='Tipos de descuento')
    no_uses = models.PositiveSmallIntegerField(verbose_name='No. de usos',null=True,blank=True)
    uses = models.PositiveSmallIntegerField(verbose_name='Usos',default=0)
    apply_all = models.BooleanField(verbose_name='Apply all products', default=False)
    min_purchase = models.PositiveSmallIntegerField(verbose_name='Minimun purchase', default=0)
    # use_types = models.CharField(max_length=1,choices=USE_TYPES,default='A',verbose_name='Tipos de usos')
    date_expiration = models.DateField(verbose_name='Fecha expiración',default=None)
    available = models.BooleanField(verbose_name='Disponible', default=True)
    status = models.BooleanField(verbose_name='Status', default=True)

    class Meta:
        db_table = 'coupons'
        verbose_name = 'Cupon'
        verbose_name_plural = 'Cupones'

    def __str__(self):
        return self.code

    def total_remaining_days(self):
        from django.utils import timezone
        return (self.date_expiration - timezone.now().today().date()).days

class CouponProduct(TimeStampedModel):
    coupon = models.ForeignKey(Coupon, related_name='products_coupons', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products_coupons', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_coupons'

    def __str__(self):
        return self.coupon.code

class ReviewProduct(TimeStampedModel):
    product = models.ForeignKey(Product,related_name='products_reviews',verbose_name='Product', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='review', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comentario')

    class Meta:
        db_table = 'review'
        ordering = ('-created',)
