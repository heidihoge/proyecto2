# Generated by Django 2.0.2 on 2018-06-01 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0011_auto_20180531_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clase',
            name='costo',
        ),
    ]
