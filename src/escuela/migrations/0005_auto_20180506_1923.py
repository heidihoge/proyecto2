# Generated by Django 2.0.2 on 2018-05-06 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20180506_1840'),
        ('escuela', '0004_auto_20180506_1814'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='asistencia',
            unique_together={('id_alumno', 'grupo', 'fecha')},
        ),
    ]
