# Generated by Django 2.0.2 on 2018-03-13 01:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('personas', '0002_auto_20180312_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='sexo',
            field=models.CharField(choices=[('F', 'FEMENINO'), ('M', 'MASCULINO')], max_length=1),
        ),
    ]
