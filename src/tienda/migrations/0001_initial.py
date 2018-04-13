# Generated by Django 2.0.2 on 2018-04-13 03:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_razon', models.CharField(default='', max_length=150)),
                ('ruc_cliente', models.IntegerField(default=0)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompraCabecera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default='', max_length=150)),
                ('proveedor', models.CharField(default='', max_length=150)),
                ('tipo_pago', models.CharField(choices=[('Contado', 'Contado'), ('Crédito', 'Crédito')], default='Contado', max_length=7)),
                ('monto_total', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CompraDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('precio', models.IntegerField(default=0)),
                ('id_cab_compra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.CompraCabecera')),
            ],
        ),
        migrations.CreateModel(
            name='Existencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('existencia_actual', models.IntegerField(default=0)),
                ('id_producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.CategoriaProducto')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('ruc', models.CharField(max_length=8, unique=True)),
                ('actividad_economica', models.CharField(blank=True, max_length=50, null=True)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('numero_timbrado', models.IntegerField(default=0)),
                ('punto_emision', models.IntegerField(default=0)),
                ('nro_inicial', models.IntegerField(default=0)),
                ('nro_final', models.IntegerField(default=0)),
                ('vigencia_desde', models.DateField(default=datetime.date.today)),
                ('vigencia_hasta', models.DateField(default=datetime.date.today)),
                ('estado', models.CharField(choices=[('A', 'ACTIVO'), ('IN', 'INACTIVO')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_pago', models.IntegerField(default=0)),
                ('saldo', models.IntegerField(default=0)),
                ('comentario', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=150)),
                ('precio', models.IntegerField(default=0)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('iva', models.DecimalField(choices=[(0.05, '5%'), (0.1, '10%'), (0, 'E')], decimal_places=2, max_digits=3)),
                ('estado', models.CharField(choices=[('A', 'ACTIVO'), ('IN', 'INACTIVO')], max_length=1)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.CategoriaProducto')),
            ],
        ),
        migrations.CreateModel(
            name='VentaCabecera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago', models.CharField(choices=[('Contado', 'Contado'), ('Crédito', 'Crédito')], default='Contado', max_length=7)),
                ('monto_total', models.IntegerField(default=0)),
                ('monto_parcial', models.IntegerField(default=0)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.Cliente')),
                ('factura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.Factura')),
            ],
        ),
        migrations.CreateModel(
            name='VentaDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('precio', models.IntegerField(default=0)),
                ('id_cab_venta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.VentaCabecera')),
                ('id_producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.Producto')),
            ],
        ),
        migrations.AddField(
            model_name='pago',
            name='id_cab_venta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tienda.VentaCabecera'),
        ),
        migrations.AddField(
            model_name='pago',
            name='id_cuenta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Cuenta'),
        ),
        migrations.AddField(
            model_name='compradetalle',
            name='id_producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tienda.Producto'),
        ),
    ]
