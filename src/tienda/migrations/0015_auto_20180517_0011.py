# Generated by Django 2.0.2 on 2018-05-17 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0014_auto_20180513_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='punto_emision',
            field=models.CharField(max_length=10),
        ),
    ]