import csv
import datetime

from django.http import HttpResponse

from tienda.models import VentaCabecera

def export_venta(resultados, fecha, fecha_fin=None, nombre='ventas-diarias'):
    response = HttpResponse(content_type='text/csv')
    fecha_1 = '{0:02}-{1:02}-{2}'.format(fecha.day, fecha.month, fecha.year)
    fecha_2 = '-{0:02}-{1:02}-{2}'.format(fecha_fin.day, fecha_fin.month, fecha_fin.year) if fecha_fin else ''
    response['Content-Disposition'] = 'attachment; filename="{0}-{1}{2}.csv"'\
        .format(nombre, fecha_1, fecha_2)

    writer = csv.writer(response)
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

    return response


def ventas_diaras():
    ventas = VentaCabecera.objects.filter(fecha=datetime.date.today(), estado__in=['A'], tipo_pago='Contado')
    resp = export_venta(ventas, datetime.date.today())
    return str(resp.content)


def compras_diaras():
    return ""


def caja_chica_diaras():
    return ""