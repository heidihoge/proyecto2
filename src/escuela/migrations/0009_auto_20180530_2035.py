# Generated by Django 2.0.2 on 2018-05-31 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0008_auto_20180530_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuenta',
            name='detalle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tienda.VentaDetalle'),
        ),
    ]