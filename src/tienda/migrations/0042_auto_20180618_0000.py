# Generated by Django 2.0.2 on 2018-06-18 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0041_auto_20180617_2351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ventacabecera',
            old_name='total_iva_exentas',
            new_name='total_grav_exentas',
        ),
    ]
