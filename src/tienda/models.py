import datetime

from django.db import models

# Create your models here.
from main.models import  Cuenta



# Tipo de documento
class Factura(models.Model):
    nombre = models.CharField(max_length=50)
    ruc = models.CharField(max_length=8, unique=True)
    actividad_economica = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)
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
    descuento= models.DecimalField(max_digits=3, decimal_places=2, default=0)
    IVA = ((0.05,'5%'),
           (0.10,'10%'),
           (0,'E'))
    iva = models.DecimalField(choices=IVA,max_digits=3, decimal_places=2)
    ESTADO = (('A', 'ACTIVO'),
           ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=1, choices=ESTADO)

    def __str__(self):
        return  self.nombre


# stock_productos

class Existencia(models.Model):
    id_producto = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE,null=True)
    existencia_actual = models.IntegerField(default=0)


# compras

class CompraCabecera(models.Model):
    descripcion = models.CharField(max_length=150,default='')
    proveedor= models.CharField(max_length=150, default='')
    fecha= models.DateField
    TIPO_PAGO = (('Contado', 'Contado'),
              ('Crédito', 'Crédito'))
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO,default='Contado')
    monto_total = models.IntegerField(default=0)

class CompraDetalle(models.Model):
    id_cab_compra= models.ForeignKey(CompraCabecera, on_delete=models.CASCADE,null=True)
    id_producto=models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True)
    cantidad = models.IntegerField(default=0)
    precio= models.IntegerField(default=0)


# cliente
class Cliente(models.Model):
    nombre_razon = models.CharField(max_length=150, default='')
    ruc_cliente = models.IntegerField(default=0)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)

# ventas
class VentaCabecera(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.SET_NULL, null=True)
    TIPO_PAGO = (('Contado', 'Contado'),
                 ('Crédito', 'Crédito'))
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO,default='Contado')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    fecha= models.DateField
    monto_total = models.IntegerField(default=0)
    monto_parcial= models.IntegerField(default=0)


class VentaDetalle(models.Model):
    id_cab_venta= models.ForeignKey(VentaCabecera, on_delete=models.CASCADE,null=True)
    id_producto=models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True)
    cantidad = models.IntegerField(default=0)
    precio= models.IntegerField(default=0)

# pagos
class Pago(models.Model):
    id_cab_venta = models.ForeignKey(VentaCabecera, on_delete=models.CASCADE, null=True)
    id_cuenta=models.ForeignKey(Cuenta, on_delete=models.SET_NULL,null=True)
    fecha_pago=models.DateField
    monto_pago = models.IntegerField(default=0)
    saldo=models.IntegerField(default=0)
    comentario= models.CharField(max_length=150)
