import datetime
import datetime

from django.contrib.auth import admin
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


# Factura
class Factura(models.Model):
    nombre = models.CharField(max_length=50)
    ruc = models.CharField(max_length=9)
    actividad_economica = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    numero_timbrado = models.IntegerField(default=0)
    punto_emision = models.CharField(max_length=10)
    nro_inicial = models.IntegerField(default=0)
    nro_final = models.IntegerField(default=0)
    vigencia_desde = models.DateField(default=datetime.date.today)
    vigencia_hasta = models.DateField(default=datetime.date.today)
    ESTADO = (('A', 'ACTIVO'),
              ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=2, choices=ESTADO, default='A')

    def __str__(self):
        return "{0} ({1}-[{2}-{3}])".format(self.numero_timbrado, self.punto_emision, self.nro_inicial, self.nro_final)

    class Meta:
        permissions = (
            ("factura_delete", "Dar de baja factura"),
            ("factura_create", "Crear factura"),
            ("factura_update", "Editar factura"),
            ("factura_list", "Listar factura"),

        )

# producto

class Producto(models.Model):
    from decimal import Decimal
    codigo = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=50)
    foto_producto = models.ImageField(upload_to='media_root', verbose_name='Foto producto', null=True, blank=True)
    descripcion = models.CharField(max_length=150)
    control_stock = models.BooleanField(default=False, blank=True)
    precio_venta = models.IntegerField(default=0)
    costo = models.IntegerField(default=0)
    IVA = ((Decimal("0.05"), '5%'),
           (Decimal("0.10"), '10%'),
           (Decimal("0.00"), 'Exentas'))
    iva = models.DecimalField(choices=IVA, max_digits=3, decimal_places=2)
    ESTADO = (('A', 'ACTIVO'),
              ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=2, choices=ESTADO)
    existencia = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        permissions = (
            ("producto_delete", "Dar de baja producto"),
            ("producto_create", "Crear producto"),
            ("producto_update", "Editar producto"),
            ("producto_list", "Listar producto"),

        )


# compras

class CompraCabecera(models.Model):
    descripcion = models.CharField(max_length=150, default='')
    ruc_proveedor = models.CharField(max_length=15, default='')
    proveedor = models.CharField(max_length=150, default='')
    fecha = models.DateField(default=datetime.date.today)
    TIPO_PAGO = (('Contado', 'Contado'),
                 ('Crédito', 'Crédito'))
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO, default='Contado')
    monto_total = models.IntegerField(default=0)
    nro_factura = models.CharField(max_length=150, default='')
    total_iva_5 = models.IntegerField(default=0)
    total_iva_10 = models.IntegerField(default=0)
    total_iva = models.IntegerField(default=0)
    total_grav_5 = models.IntegerField(default=0)
    total_grav_10 = models.IntegerField(default=0)
    total_grav_exentas = models.IntegerField(default=0)

    def __str__(self):
        return int(self.id)



class CompraDetalle(models.Model):
    compra = models.ForeignKey(CompraCabecera, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=250)
    monto_5 = models.IntegerField(default=0)
    monto_10 = models.IntegerField(default=0)
    monto_exento = models.IntegerField(default=0)



# cliente
class Cliente(models.Model):
    nombre_razon = models.CharField(max_length=150, default='')
    ruc_cliente = models.CharField(primary_key=True, max_length=15)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.ruc_cliente + " (" + self.nombre_razon + ")"

    class Meta:
        permissions = (
            ("cliente_delete", "Dar de baja cliente"),
            ("cliente_create", "Crear cliente"),
            ("cliente_update", "Editar cliente"),
            ("clientes_list", "Listar cliente"),

        )

# metodo de pago = tarjeta, cheque, efectivo
# Forma de pago = contado , credito
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
    tipo_pago = models.CharField(max_length=7, choices=TIPO_PAGO, default='Contado')

    credito_plazo = models.IntegerField(default=0)

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(default=datetime.date.today)
    monto_total = models.IntegerField(default=0)
    total_iva_5 = models.IntegerField(default=0)
    total_iva_10 = models.IntegerField(default=0)
    total_grav_5 = models.IntegerField(default=0)
    total_grav_10 = models.IntegerField(default=0)
    total_grav_exentas = models.IntegerField(default=0)
    total_iva = models.IntegerField(default=0)
    ESTADO = (('A', 'ACTIVO'),
              ('IN', 'INACTIVO'),
              ('P', 'PENDIENTE'),
              )
    estado = models.CharField(max_length=2, choices=ESTADO, default='A')

    def __str__(self):
        return str(self.id)


class VentaDetalle(models.Model):
    venta = models.ForeignKey(VentaCabecera, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    detalle = models.CharField(max_length=150, default='')
    cantidad = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)
    monto_5 = models.IntegerField(default=0)
    monto_10 = models.IntegerField(default=0)
    monto_exento = models.IntegerField(default=0)



class OperacionCaja(models.Model):
    fecha = models.DateField(default=datetime.date.today)
    concepto = models.CharField(max_length=150, default='')
    descripcion = models.CharField(max_length=150, default='')
    monto = models.IntegerField(default=0)
    TIPO_TRANSACCION = (('ENTRADA', 'ENTRADA'),
                       ('SALIDA', 'SALIDA'))
    tipo_transaccion = models.CharField(max_length=7, choices=TIPO_TRANSACCION, default='ENT')

    def __str__(self):
        return str(self.fecha)

    class Meta:
        indexes = [
            models.Index(fields=['fecha', 'tipo_transaccion']),
        ]


# PAGOS

class Pago(models.Model):
    venta = models.ForeignKey(VentaCabecera, on_delete=models.SET_NULL, null=True,blank=True)

    pago_efectivo = models.BooleanField(default=False)
    pago_tarjeta = models.BooleanField(default=False)
    pago_cheque = models.BooleanField(default=False)
    monto =  models.IntegerField(default=0,blank=True)
    monto_efectivo = models.IntegerField(default=0,blank=True)
    monto_efectivo_abonado = models.IntegerField(default=0,blank=True)
    monto_efectivo_vuelto = models.IntegerField(default=0,blank=True)
    monto_tarjeta = models.IntegerField(default=0,blank=True)
    monto_cheque = models.IntegerField(default=0,blank=True)

    # si es tarjeta

    # Tarjetas de Crédito del sistema Bancard; Visa, MasterCard, Credifielco, Diners Club International, American Express y Discover.

    # Visa – MasterCard – Bancard Check – Credifielco – Discover – American Express – Diners Club. Visa Débito – Visa Electrón – Maestro – Infonet.


    CLASIFICACION_TARJETA = (('INFONET-DEBITO', 'INFONET-DEBITO'),
                             ('INFONET-CREDITO', 'INFONET-CREDITO'))
    tarjeta = models.CharField(max_length=25, choices=CLASIFICACION_TARJETA, default='',blank=True,null=True)
    nro_autorizacion = models.CharField(max_length=150, default='', null=True,blank=True)
    ultimos_tarjeta = models.CharField(max_length=150, default='', null=True,blank=True)


    # si es cheque >Entidad bancaria, número de cuenta bancaria ,serie cheque,número de cheque, fecha emisión,fecha  vencimiento

    banco = models.CharField(max_length=150, default='', null=True,blank=True)
    nro_cuenta = models.CharField(max_length=150, default='', null=True,blank=True)
    librador = models.CharField(max_length=150, default='', null=True,blank=True)
    serie_cheque = models.CharField(max_length=150, default='', null=True,blank=True)
    nro_cheque = models.CharField(max_length=150, default='', null=True,blank=True)
    fecha_emision = models.DateField( null=True,blank=True)
    fecha_venc = models.DateField( null=True,blank=True)

class Recibo(models.Model):
    fecha = models.DateField(default=datetime.date.today)
    nro_recibo = models.CharField(max_length=32)
    nombre_cliente = models.CharField(max_length=150, default='')

    venta = models.ForeignKey(VentaCabecera, on_delete=models.SET_NULL, null=True,blank=True)

    pago_efectivo = models.BooleanField(default=False)
    pago_tarjeta = models.BooleanField(default=False)
    pago_cheque = models.BooleanField(default=False)
    monto =  models.IntegerField(default=0,blank=True)
    monto_efectivo = models.IntegerField(default=0,blank=True)
    monto_efectivo_abonado = models.IntegerField(default=0,blank=True)
    monto_efectivo_vuelto = models.IntegerField(default=0,blank=True)
    monto_tarjeta = models.IntegerField(default=0,blank=True)
    monto_cheque = models.IntegerField(default=0,blank=True)

    # si es tarjeta

    # Tarjetas de Crédito del sistema Bancard; Visa, MasterCard, Credifielco, Diners Club International, American Express y Discover.

    # Visa – MasterCard – Bancard Check – Credifielco – Discover – American Express – Diners Club. Visa Débito – Visa Electrón – Maestro – Infonet.


    CLASIFICACION_TARJETA = (('INFONET-DEBITO', 'INFONET-DEBITO'),
                             ('INFONET-CREDITO', 'INFONET-CREDITO'))
    tarjeta = models.CharField(max_length=25, choices=CLASIFICACION_TARJETA, default='',blank=True,null=True)
    nro_autorizacion = models.CharField(max_length=150, default='', null=True,blank=True)
    ultimos_tarjeta = models.CharField(max_length=150, default='', null=True,blank=True)

    # si es cheque >Entidad bancaria, número de cuenta bancaria ,serie cheque,número de cheque, fecha emisión,fecha  vencimiento

    banco = models.CharField(max_length=150, default='', null=True,blank=True)
    nro_cuenta = models.CharField(max_length=150, default='', null=True,blank=True)
    librador = models.CharField(max_length=150, default='', null=True,blank=True)
    serie_cheque = models.CharField(max_length=150, default='', null=True,blank=True)
    nro_cheque = models.CharField(max_length=150, default='', null=True,blank=True)
    fecha_emision = models.DateField( null=True,blank=True)
    fecha_venc = models.DateField( null=True,blank=True)
