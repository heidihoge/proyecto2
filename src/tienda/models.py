import datetime
import datetime

from django.db import models

# Create your models here.



# Factura
class Factura(models.Model):
    nombre = models.CharField(max_length=50)
    ruc = models.CharField(max_length=9, unique=True)
    actividad_economica = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    numero_timbrado = models.IntegerField(default=0)
    punto_emision= models.CharField(max_length=10)
    nro_inicial=models.IntegerField(default=0)
    nro_final=models.IntegerField(default=0)
    vigencia_desde=models.DateField(default=datetime.date.today)
    vigencia_hasta= models.DateField(default=datetime.date.today)
    ESTADO = (('A', 'ACTIVO'),
              ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=1, choices=ESTADO, default='A')

    def __str__(self):
        return "{0} ({1}-[{2}-{3}])".format(self.numero_timbrado, self.punto_emision, self.nro_inicial, self.nro_final)




# producto

class Producto(models.Model):
    from decimal import Decimal
    codigo = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=50)
    foto_producto = models.ImageField(upload_to='media_root', verbose_name='Foto producto', null=True,blank=True)
    descripcion = models.CharField(max_length=150)
    control_stock = models.BooleanField(default=False, blank=True)
    precio_venta = models.IntegerField(default=0)
    costo = models.IntegerField(default=0)
    IVA = ((Decimal("0.05"),'5%'),
           (Decimal("0.10"),'10%'),
           (Decimal("0.00"),'Exentas'))
    iva = models.DecimalField(choices=IVA,max_digits=3, decimal_places=2)
    ESTADO = (('A', 'ACTIVO'),
           ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=2, choices=ESTADO)
    existencia = models.IntegerField(default=0)

    def __str__(self):
        return  self.nombre



# compras

class CompraCabecera(models.Model):
    descripcion = models.CharField(max_length=150,default='')
    proveedor= models.CharField(max_length=150, default='')
    fecha = models.DateField(default=datetime.date.today)
    TIPO_PAGO = (('Contado', 'Contado'),
              ('Crédito', 'Crédito'))
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO,default='Contado')
    monto_total = models.IntegerField(default=0)
    nro_factura = models.CharField(max_length=150, default='')
    total_iva_5 = models.IntegerField(default=0)
    total_iva_10 = models.IntegerField(default=0)
    total_iva = models.IntegerField(default=0)
    def __str__(self):
        return  self.id

class CompraDetalle(models.Model):
    compra = models.ForeignKey(CompraCabecera, on_delete=models.CASCADE,null=True)
    producto = models.CharField(max_length=250,null=True)
    cantidad = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)


# cliente
class Cliente(models.Model):
    nombre_razon = models.CharField(max_length=150, default='')
    ruc_cliente = models.CharField(primary_key=True, max_length=15)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.ruc_cliente + " (" + self.nombre_razon + ")"

# ventas
class VentaCabecera(models.Model):
    talonario_factura = models.ForeignKey(Factura, on_delete=models.SET_NULL, null=True)
    nro_factura = models.CharField(max_length=150, default='')

    # Separamos en 2 para poder utilizar en los queries
    # Por ejemplo, obtener el maximo y el siguiente numero de factura.
    nro_factura_punto_emision = models.CharField(max_length=10, default='')
    nro_factura_numero = models.IntegerField(default=0)

    TIPO_PAGO = (('Contado', 'Contado'),
                 ('Crédito', 'Crédito'))
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO,default='Contado')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(default=datetime.date.today)
    monto_total = models.IntegerField(default=0)
    total_iva_5 = models.IntegerField(default=0)
    total_iva_10 = models.IntegerField(default=0)
    total_iva_exentas = models.IntegerField(default=0)
    total_iva = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)

class VentaDetalle(models.Model):
    venta = models.ForeignKey(VentaCabecera, on_delete=models.CASCADE,null=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True)
    detalle = models.CharField(max_length=150, default='')
    cantidad = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)
    monto_5 = models.IntegerField(default=0)
    monto_10 = models.IntegerField(default=0)
    monto_exento = models.IntegerField(default=0)

