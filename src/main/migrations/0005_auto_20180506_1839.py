# Generated by Django 2.0.2 on 2018-05-06 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180506_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='estado',
            field=models.CharField(choices=[('A', 'ACTIVO'), ('IN', 'INACTIVO')], default='ACTIVO', max_length=1),
        ),
    ]
