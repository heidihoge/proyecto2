import csv
import datetime

from dateutil.relativedelta import relativedelta
from django.db import connection
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from escuela.models import Grupo
from escuela.utils import dictfetch
from proyecto2 import settings
from tienda.models import CompraCabecera, VentaCabecera


def get_date(fecha_string):
    return datetime.datetime.strptime(fecha_string, settings.DATE_INPUT_FORMATS[0]).date()

def get_month(fecha_mes):
    return datetime.datetime.strptime(fecha_mes, settings.MONTH_INPUT_FORMATS[0]).date()

# COMPRA


def export_compra(resultados, totales, fecha):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="libro-compra-{0:02}-{1}.csv"'\
        .format(fecha.month, fecha.year)

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Nro Factura', 'Ruc', 'Proveedor', 'Exentas',
                     'Gravada 5%', 'IVA 5%', 'Gravada 10%', 'IVA 10%', 'Total'])

    for resultado in resultados:
        writer.writerow([resultado.fecha, str(resultado.nro_factura), resultado.ruc_proveedor,
                         resultado.proveedor, resultado.total_grav_exentas,
                         resultado.total_grav_5, resultado.total_iva_5,
                         resultado.total_grav_10, resultado.total_iva_10, resultado.monto_total ])

    writer.writerow(['', '', '', 'Total:', totales['exentas'], totales['grav_5'], totales['iva_5'],
                    totales['grav_10'], totales['iva_10'], totales['total']])
    return response

def compra(request):


    accion = request.GET.get('action', 'Ver')

    fecha_inicio = request.GET.get('mes', None)
    if not fecha_inicio:
        fecha_inicio = datetime.date.today().replace(day=1)
    else:
        fecha_inicio = get_month(fecha_inicio)

    fecha_fin = (fecha_inicio + relativedelta(months=1, days=-1))

    resultados = CompraCabecera.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)

    totales = resultados.aggregate(exentas=Sum('total_grav_exentas'), #
                         grav_5=Sum('total_grav_5'),#
                         grav_10=Sum('total_grav_10'),#
                         iva_5=Sum('total_iva_5'),#
                         iva_10=Sum('total_iva_10'),#
                         total=Sum('monto_total'))

    if accion == 'Excel':
        return export_compra(resultados, totales, fecha_inicio)


    context = { 'mes': '{0:02}/{1}'.format(fecha_inicio.month, fecha_inicio.year),
                'resultados': resultados, 'totales': totales }
    return render(request, "libro_compra.html", context)

# VENTA

def export_venta(resultados, totales, fecha):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="libro-venta-{0:02}-{1}.csv"'\
        .format(fecha.month, fecha.year)

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Nro Factura', 'Ruc Cliente', 'Nombre o Razón', 'Exentas',
                     'Gravada 5%', 'IVA 5%', 'Gravada 10%', 'IVA 10%', 'Total'])

    for resultado in resultados:
        writer.writerow([resultado.fecha, str(resultado.nro_factura), resultado.cliente.ruc_cliente,
                         resultado.cliente.nombre_razon, resultado.total_grav_exentas,
                         resultado.total_grav_5, resultado.total_iva_5,
                         resultado.total_grav_10, resultado.total_iva_10, resultado.monto_total ])

    writer.writerow(['', '', '', 'Total:', totales['exentas'], totales['grav_5'], totales['iva_5'],
                    totales['grav_10'], totales['iva_10'], totales['total']])
    return response

def venta(request):

    accion = request.GET.get('action', 'Ver')

    fecha_inicio = request.GET.get('mes', None)
    if not fecha_inicio:
        fecha_inicio = datetime.date.today().replace(day=1)
    else:
        fecha_inicio = get_month(fecha_inicio)

    fecha_fin = (fecha_inicio + relativedelta(months=1, days=-1))

    resultados = VentaCabecera.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin)

    totales = resultados.aggregate(exentas=Sum('total_grav_exentas'), #
                         grav_5=Sum('total_grav_5'),#
                         grav_10=Sum('total_grav_10'),#
                         iva_5=Sum('total_iva_5'),#
                         iva_10=Sum('total_iva_10'),#
                         total=Sum('monto_total'))

    if accion == 'Excel':
        return export_venta(resultados, totales, fecha_inicio)


    context = { 'mes': '{0:02}/{1}'.format(fecha_inicio.month, fecha_inicio.year),
                'resultados': resultados, 'totales': totales }
    return render(request, "libro_venta.html", context)


# ASISTENCIA

def export_asistencia(resultados, fecha, grupo):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asistencia-{0:02}-{1}-{2}.csv"'\
        .format(fecha.month, fecha.year, str(grupo).replace(' ','-').replace(':','-').replace('(', '').replace(')',''))

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Cedula', 'Nombre', 'Asistencia', 'Comentario'])

    for resultado in resultados:
        writer.writerow([resultado['fecha'], resultado['cedula'], resultado['nombre'],
                         resultado['asistencia'], resultado['comentario']])

    return response


def asistencia(request):
    grupo_id = request.GET.get('grupo', None)
    action = request.GET.get('action', 'Ver')
    resultados = []
    dates = []
    alumnos = []
    try:
        grupo = Grupo.objects.get(id=int(grupo_id))
    except:
        grupo = None

    fecha_inicio = request.GET.get('mes', None)
    if not fecha_inicio:
        fecha_inicio = datetime.date.today().replace(day=1)
    else:
        fecha_inicio = get_month(fecha_inicio)

    fecha_fin = (fecha_inicio + relativedelta(months=1, days=-1))

    if grupo:
        query = """
        SELECT a.fecha, al.cedula, al.apellido || ', ' || al.nombre as nombre, 
        case when a.presente then 'Presente' else 'Ausente' end as asistencia, 
        a.comentario from escuela_asistencia a
        JOIN main_persona al on a.id_alumno_id = al.id
        WHERE grupo_id = %(grupo_id)s
        AND a.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
        ORDER BY a.fecha DESC, al.apellido
        """
        cursor = connection.cursor()
        cursor.execute(query, {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'grupo_id': grupo.id})
        resultados = dictfetch(cursor, 1000, 0)

        if action == 'Excel':
            return export_asistencia(resultados, fecha_inicio, grupo)

        alumnos = {}
        for resultado in resultados:
            if not resultado['nombre'] in alumnos:
                alumnos[resultado['nombre']] = {
                    "Ausente": 0,
                    "Presente": 0,
                    "Nombre": resultado['nombre']
                }
            alumnos[resultado['nombre']][resultado['asistencia']] += 1

        alumnos = [alumnos[alumno] for alumno in alumnos]


    context = {'mes': '{0:02}/{1}'.format(fecha_inicio.month, fecha_inicio.year),
               'grupo': grupo, 'resultados': resultados, 'alumnos': alumnos}
    return render(request, "asistencia.html", context)

# BALANCE

def export_balance(resultados, fecha):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance-{0:02}-{1}.csv"'.format(fecha.month, fecha.year)

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Monto', 'Tipo de transacción'])

    for resultado in resultados:
        writer.writerow([resultado['fecha'], resultado['monto'], resultado['tipo_transaccion']])

    return response

def balance(request):

    accion = request.GET.get('action', 'Ver')

    fecha_inicio = request.GET.get('mes', None)
    if not fecha_inicio:
        fecha_inicio = datetime.date.today().replace(day=1)
    else:
        fecha_inicio = get_month(fecha_inicio)

    fecha_fin = (fecha_inicio + relativedelta(months=1, days=-1))

    query = """
        select fecha, sum(monto) monto, tipo_transaccion from (
      select fecha, monto, tipo_transaccion from tienda_operacioncaja
    UNION
    select fecha, monto_total, 'SALIDA' as tipo_transaccion from tienda_compracabecera
    UNION
    select fecha, monto_total, 'ENTRADA' as tipo_transaccion from tienda_ventacabecera) e
    where e.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
    GROUP BY fecha, tipo_transaccion
    ORDER BY fecha DESC 
    """
    cursor = connection.cursor()
    cursor.execute(query, { 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin })
    resultados = dictfetch(cursor, 100, 0)

    if accion == 'Excel':
        return export_balance(resultados, fecha_inicio)

    ingreso = sum(map(lambda x:x["monto"] , filter(lambda x: x["tipo_transaccion"] == 'ENTRADA', resultados)))
    egreso = sum(map(lambda x:x["monto"] , filter(lambda x: x["tipo_transaccion"] == 'SALIDA', resultados)))
    ganancia = ingreso - egreso



    datequery = """
        select dd::date as date from generate_series
        ( %(fecha_inicio)s
        , %(fecha_fin)s
        , '1 day'::interval) dd
    """
    cursor.execute(datequery, {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
    dates = dictfetch(cursor, 100, 0)

    context = { 'mes': '{0:02}/{1}'.format(fecha_inicio.month, fecha_inicio.year),
                'resultados': resultados, 'dates': dates, 'ingreso': ingreso, 'egreso': egreso, 'ganancia': ganancia }
    return render(request, "balance.html", context)