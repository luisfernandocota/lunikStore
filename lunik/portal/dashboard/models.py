from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class Address(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='address', on_delete=models.CASCADE)
    name = models.CharField(max_length=130, verbose_name='Name', null=True)
    address = models.CharField(max_length=120,verbose_name='Address')
    zip_code = models.CharField(max_length=5,verbose_name='Zip code')
    num_ext = models.CharField(max_length=5, verbose_name='Num Ext')
    num_int = models.CharField(max_length=5, verbose_name='Num Int')
    city = models.CharField(max_length=80,verbose_name='City')
    state = models.CharField(max_length=30,verbose_name='State')
    suburb = models.CharField(max_length=50, verbose_name='Suburb')
    default = models.BooleanField(default=False, verbose_name="Predeterminada")
    status = models.BooleanField(verbose_name='Activo', default=True)
    class Meta:
        db_table = 'address'
        verbose_name = 'Address'
        ordering = ['-created']

    def __str__(self):
        return self.name