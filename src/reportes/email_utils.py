import csv
import datetime
from io import StringIO

from django.http import HttpResponse

from tienda.models import VentaCabecera, CompraCabecera, OperacionCaja


def export_venta(resultados, fecha, fecha_fin=None, nombre='ventas-diarias'):
    csvfile = StringIO()

    writer = csv.writer(csvfile)
    writer.writerow(['Fecha', 'Nro Factura', 'Tipo de pago', 'Ruc Cliente', 'Cliente', 'Gravada 10%', 'IVA 10%',
                     'Gravada 5%', 'IVA 5%', 'Exentas', 'Total IVA', 'Monto Total', 'Estado'])

    def texto_estado(estado):
        if estado == 'A':
            return 'Pagado'
        if estado == 'P':
            return 'Pendiente'
        if estado == 'IN':
            return 'Cancelado'
        return estado

    for resultado in resultados:
        writer.writerow([resultado.fecha, str(resultado.nro_factura), resultado.tipo_pago,
                         resultado.cliente.ruc_cliente,
                         resultado.cliente.nombre_razon, resultado.total_grav_10,
                         resultado.total_iva_10, resultado.total_grav_5,
                         resultado.total_iva_5, resultado.total_grav_exentas, resultado.total_iva,
                         resultado.monto_total, texto_estado(resultado.estado)])

    return csvfile


def ventas_diaras():
    ventas = VentaCabecera.objects.filter(fecha=datetime.date.today(), estado__in=['A'], tipo_pago='Contado')
    resp = export_venta(ventas, datetime.date.today())
    return resp.getvalue()



def export_compra(resultados, fecha, fecha_fin=None, nombre='compras-diarias'):
    csvfile = StringIO()

    writer = csv.writer(csvfile)
    writer.writerow(['Fecha', 'Nro Factura', 'Descripcion', 'Ruc Proveedor', 'Nombre Proveedor', 'Gravada 10%', 'IVA 10%',
                    'Gravada 5%', 'IVA 5%', 'Exentas', 'Total IVA', 'Monto Total'])



    for resultado in resultados:
        writer.writerow([resultado.fecha, str(resultado.nro_factura), resultado.tipo_pago,
                         resultado.ruc_proveedor,
                         resultado.proveedor, resultado.total_grav_10,
                         resultado.total_iva_10, resultado.total_grav_5,
                         resultado.total_iva_5, resultado.total_grav_exentas, resultado.total_iva,
                         resultado.monto_total])

    return csvfile


def compras_diaras():
    compras = CompraCabecera.objects.filter(fecha=datetime.date.today())
    resp = export_compra(compras, datetime.date.today())
    return resp.getvalue()


def export_operaciones(operaciones, fecha):
    csvfile = StringIO()
    writer = csv.writer(csvfile)
    writer.writerow(['Fecha', 'Tipo transaccion', 'Monto', 'Concepto', 'Descripcion'])

    for operacion in operaciones:
        writer.writerow([operacion.fecha, operacion.tipo_transaccion, operacion.monto,
                         operacion.concepto, operacion.descripcion])

    return csvfile

def caja_chica_diaras():
    operaciones = OperacionCaja.objects.filter(fecha=datetime.date.today())
    resp = export_operaciones(operaciones, datetime.date.today())
    return resp.getvalue()
