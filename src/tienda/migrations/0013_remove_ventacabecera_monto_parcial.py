# Generated by Django 2.0.2 on 2018-05-13 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0012_auto_20180513_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ventacabecera',
            name='monto_parcial',
        ),
    ]
