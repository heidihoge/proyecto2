# Generated by Django 2.0.2 on 2018-05-20 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0018_auto_20180520_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventadetalle',
            name='precio',
            field=models.IntegerField(default=0),
        ),
    ]
