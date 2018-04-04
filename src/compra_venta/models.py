import datetime

from django.db import models

# Create your models here.
from main.models import  Persona, Proveedor, Cuenta



# Tipo de documento
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)


class Timbrado(models.Model):
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True)
    id_tipo_documento= models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, null=True)
    numero_timbrado = models.IntegerField(default=0)
    punto_emision= models.IntegerField(default=0)
    nro_inicial=models.IntegerField(default=0)
    nro_final=models.IntegerField(default=0)
    vigencia_desde=models.DateField
    vigencia_hasta= models.DateField
    ESTADO = (('A', 'ACTIVO'),
              ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=1, choices=ESTADO)



# categoriaProdutos
class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)


# producto

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL,null=True)
    precio = models.IntegerField(default=0)
    iva = models.IntegerField(default=0)
    ESTADO = (('A', 'ACTIVO'),
           ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=1, choices=ESTADO)

    def __str__(self):
        return  self.nombre


# stock_productos

class Existencia(models.Model):
    id_producto = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE,null=True)
    existencia_actual = models.IntegerField(default=0)
    existencia_minima=models.IntegerField(default=0)
    existencia_maxima =models.IntegerField(default=0)

# compras
class TipoPago(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)


# compras

class CompraCabecera(models.Model):
    id_proveedor=models.ForeignKey(Proveedor, on_delete=models.SET_NULL,null=True)
    fecha= models.DateField
    monto_total = models.IntegerField(default=0)
    tipo_pago= models.ForeignKey(TipoPago, on_delete=models.SET_NULL,null=True)

class CompraDetalle(models.Model):
    id_cab_compra= models.ForeignKey(CompraCabecera, on_delete=models.CASCADE,null=True)
    id_producto=models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True)
    cantidad = models.IntegerField(default=0)
    precio= models.IntegerField(default=0)
    sub_total=models.IntegerField(default=0)


# ventas
class VentaCabecera(models.Model):
    id_cliente=models.ForeignKey(Persona, on_delete=models.SET_NULL,null=True)
    factura = models.ForeignKey(Timbrado, on_delete=models.CASCADE)
    fecha= models.DateField
    monto_total = models.IntegerField(default=0)
    tipo_pago = models.ForeignKey(TipoPago, on_delete=models.SET_NULL, null=True)


class VentaDetalle(models.Model):
    id_cab_venta= models.ForeignKey(VentaCabecera, on_delete=models.CASCADE,null=True)
    id_producto=models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True)
    cantidad = models.IntegerField(default=0)
    precio= models.IntegerField(default=0)
    sub_total=models.IntegerField(default=0)



# pagos
class Pago(models.Model):
    id_cab_venta = models.ForeignKey(VentaCabecera, on_delete=models.CASCADE, null=True)
    id_cuenta=models.ForeignKey(Cuenta, on_delete=models.SET_NULL,null=True)
    fecha_pago=models.DateField
    monto_pago = models.IntegerField(default=0)
    saldo=models.IntegerField(default=0)
    comentario= models.CharField(max_length=150)
