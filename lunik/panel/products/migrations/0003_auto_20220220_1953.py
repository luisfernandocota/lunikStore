# Generated by Django 2.2.4 on 2022-02-21 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productproperty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productproperty',
            name='gain',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Gain'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='margin',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Margin'),
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Price'),
        ),
    ]
