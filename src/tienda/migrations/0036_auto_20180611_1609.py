# Generated by Django 2.0.2 on 2018-06-11 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0035_auto_20180611_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='tarjeta',
            field=models.CharField(blank=True, choices=[('INFONET-DEBITO', 'INFONET-DEBITO'), ('INFONET-CREDITO', 'INFONET-CREDITO')], default='', max_length=25, null=True),
        ),
    ]