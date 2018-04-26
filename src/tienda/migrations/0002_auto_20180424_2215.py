# Generated by Django 2.0.2 on 2018-04-25 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='existencia',
            name='id_producto',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='precio',
            new_name='costo',
        ),
        migrations.AddField(
            model_name='producto',
            name='codigo',
            field=models.CharField(default='A', max_length=8, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='existencia',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='foto_producto',
            field=models.ImageField(blank=True, null=True, upload_to='media_root', verbose_name='Foto producto'),
        ),
        migrations.AddField(
            model_name='producto',
            name='precio_venta',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Existencia',
        ),
    ]
