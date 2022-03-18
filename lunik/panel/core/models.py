from django.db import models

# class State(models.Model):
#     code = models.CharField(max_length=2, verbose_name='Código')
#     name = models.CharField(max_length=100, verbose_name='Estado')
#     abrev = models.CharField(max_length=10, verbose_name='Abreviatura')
#     status = models.BooleanField(verbose_name='status',default=True)
#
#     class Meta:
# 	    db_table = 'states'
#
#     def __str__(self):
#         return self.name
#
# class Municipality(models.Model):
#     state = models.ForeignKey(State,related_name='municipalities',on_delete=models.CASCADE,db_index=True)
#     code = models.CharField(max_length=3, verbose_name='Código')
#     name = models.CharField(max_length=100, verbose_name='Municipio')
#     status = models.BooleanField(verbose_name='status',default=True)
#
#     class Meta:
# 	    db_table = 'states_municipalities'
#
#     def __str__(self):
#         return self.name
#
# class Locality(models.Model):
#     municipality = models.ForeignKey(Municipality,related_name='localities',on_delete=models.CASCADE,db_index=True)
#     code = models.CharField(max_length=4, verbose_name='Código')
#     name = models.CharField(max_length=250, verbose_name='Localidad')
#     latitude = models.CharField(max_length=15, verbose_name='Latitud')
#     longitude = models.CharField(max_length=15, verbose_name='Longitud')
#     altitude = models.CharField(max_length=15, verbose_name='Altitud')
#     card = models.CharField(max_length=10, verbose_name='Cve Carta')
#     ambit = models.CharField(max_length=1, verbose_name='Ámbito')
#     population = models.IntegerField(verbose_name='Población')
#     male = models.IntegerField(verbose_name='Masculino')
#     female = models.IntegerField(verbose_name='Femenino')
#     households = models.IntegerField(verbose_name='Viviendas')
#     lat = models.DecimalField(max_digits=10,decimal_places=7,verbose_name='Latitud en dígitos')
#     lng = models.DecimalField(max_digits=10,decimal_places=7,verbose_name='Longitud en dígitos')
#     status = models.BooleanField(verbose_name='status',default=True)
#
#     class Meta:
# 	    db_table = 'states_municipalities_localities'
#
#     def __str__(self):
#         return self.name
