# Generated by Django 2.2.4 on 2022-02-21 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20220221_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productproperty',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='products_properties', to='products.Product'),
        ),
    ]
