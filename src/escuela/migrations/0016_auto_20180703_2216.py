# Generated by Django 2.0.2 on 2018-07-03 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0015_auto_20180702_2149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupo',
            options={'permissions': (('grupo_delete', 'Dar de baja grupo'),)},
        ),
    ]
