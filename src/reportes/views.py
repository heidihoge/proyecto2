import csv
import datetime

from dateutil.relativedelta import relativedelta
from django.db import connection
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse, request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
from escuela.models import Grupo, Clase
from escuela.utils import dictfetch
from main.models import Persona
from proyecto2 import settings
from tienda.models import CompraCabecera, VentaCabecera, Pago


def get_date(fecha_string):
    return datetime.datetime.strptime(fecha_string, settings.DATE_INPUT_FORMATS[0]).date()

def get_month(fecha_mes):
    return datetime.datetime.strptime(fecha_mes, settings.MONTH_INPUT_FORMATS[0]).date()

# ALUMNOS POR GRUPO

#@login_required() #permisos para login
def export_alumnos_por_grupo(resultados, fecha):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnos-por-grupo-{0:02}-{1:02}-{2}.csv"'\
        .format(fecha.day, fecha.month, fecha.year)

    writer = csv.writer(response)
    writer.writerow(['Grupo', 'Profesor', 'Curso', 'Cupo máximo', 'Cantidad de alumnos'])

    for resultado in resultados:
        writer.writerow([resultado['grupo'].grupo_desc(), resultado['profesor'], resultado['curso'],
                        resultado['grupo'].cupo_maximo, resultado['cantidad']])

    return response

#@login_required() #permisos para login
def to_grupo_map(resultado):
    return {
        "grupo": Grupo(
            cupo_maximo=resultado['cupo_maximo'],
            hora_fin=resultado['hora_fin'],
            hora_inicio=resultado['hora_inicio'],
            lunes=resultado['lunes'],
            martes=resultado['martes'],
            miercoles=resultado['miercoles'],
            jueves=resultado['jueves'],
            viernes=resultado['viernes'],
            sabado=resultado['sabado'],
            domingo=resultado['domingo'],
        ),
        "profesor": "{1}, {0}".format(resultado['nombre'], resultado['apellido']),
        "curso": resultado['nombre_curso'],
        "cantidad": resultado['cantidad']
    }

#@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
def alumnos_por_grupo(request):

    accion = request.GET.get('action', None)

    fecha = datetime.date.today()

    query = """
    select
      g.cupo_maximo,
      g.hora_fin,
      g.hora_inicio,
      g.lunes,
      g.martes,
      g.miercoles,
      g.jueves,
      g.viernes,
      g.sabado,
      g.domingo,
      prof.nombre as nombre,
      prof.apellido as apellido,
      c.nombre as nombre_curso,
      count.cantidad
    from (
           select
             grupo_id,
             count(*) as cantidad
           from escuela_inscripcion
           where estado = 'A'
           group by grupo_id
         ) count
      join escuela_grupo g on count.grupo_id = g.id
      join escuela_clase c on g.id_clase_id = c.id
      join main_persona prof on prof.id = g.id_profesor_id
    order by c.nombre, g.hora_inicio;
    """

    cursor = connection.cursor()
    cursor.execute(query, {})
    resultados = dictfetch(cursor, 1000, 0)

    if accion == 'Excel':
        return export_alumnos_por_grupo(map(to_grupo_map, resultados), fecha)

    context = { "resultados": map(to_grupo_map, resultados), 'fecha': fecha }

    return render(request, "alumnos_por_grupo.html", context)
# COMPRA


#@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
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


#@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
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

#@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
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


@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
def venta(request):

    accion = request.GET.get('action', 'Ver')

    fecha_inicio = request.GET.get('mes', None)
    if not fecha_inicio:
        fecha_inicio = datetime.date.today().replace(day=1)
    else:
        fecha_inicio = get_month(fecha_inicio)

    fecha_fin = (fecha_inicio + relativedelta(months=1, days=-1))

    resultados = VentaCabecera.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin, estado='A')

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

#@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
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


@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
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
#@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
def export_balance(resultados, fecha):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance-{0:02}-{1}.csv"'.format(fecha.month, fecha.year)

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Monto', 'Tipo de transacción'])

    for resultado in resultados:
        writer.writerow([resultado['fecha'], resultado['monto'], resultado['tipo_transaccion']])

    return response


@login_required() #permisos para login
@permission_required('reporte.balance', raise_exception=True)
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
    select fecha, monto_total, 'ENTRADA' as tipo_transaccion 
      from tienda_ventacabecera where estado = 'A' and tipo_pago = 'Contado' 
      UNION 
    select r.fecha,  r.monto, 'ENTRADA' as tipo_transaccion from tienda_ventacabecera t
      join tienda_recibo r on t.id = r.venta_id where t.estado in ('A', 'P') and t.tipo_pago = 'Crédito'
        ) e
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






# pagos en tarjetas
#@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
def export_tarjeta_csv(pagos):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte.csv"'

    writer = csv.writer(response)
    writer.writerow(['venta', 'monto', 'tarjeta','nro_autorizacion','ultimos_tarjeta'])

    for pago in pagos:
        writer.writerow(list(pago))

    return response

@login_required() #permisos para login
#@permission_required('reporte.alumnos_por_grupo', raise_exception=True)
def list_pagos_fechas(request):
    fecha_desde = request.GET.get('fecha_desde', None)
    fecha_hasta = request.GET.get('fecha_hasta', None)
    accion = request.GET.get('action', 'Ver')

    if not fecha_desde :
        fecha_desde = datetime.date.today()
    else:
        fecha_desde = datetime.datetime.strptime(fecha_desde, settings.DATE_INPUT_FORMATS[0]).date()

    if not fecha_hasta :
        fecha_hasta = datetime.date.today()
    else:
        fecha_hasta = datetime.datetime.strptime(fecha_hasta, settings.DATE_INPUT_FORMATS[0]).date()

    pagos = Pago.objects.filter(venta__estado='A',venta__fecha__gte=fecha_desde,
                                venta__fecha__lte=fecha_hasta ,pago_tarjeta=True)\
        .values_list('venta__fecha', 'monto','tarjeta','nro_autorizacion','ultimos_tarjeta')

    context = {'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta,
               'pagos': pagos}

    if accion == 'Excel':
        return export_tarjeta_csv(pagos)

    return render(request, "pagos-rango-fecha.html", context)




