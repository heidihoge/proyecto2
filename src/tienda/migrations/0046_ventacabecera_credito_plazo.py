# Generated by Django 2.0.2 on 2018-07-01 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0045_auto_20180624_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventacabecera',
            name='credito_plazo',
            field=models.IntegerField(default=0),
        ),
    ]