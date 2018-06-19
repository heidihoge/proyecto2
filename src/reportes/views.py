import datetime

from dateutil.relativedelta import relativedelta
from django.db import connection
from django.shortcuts import render

# Create your views here.
from escuela.utils import dictfetch
from proyecto2 import settings

def get_date(fecha_string):
    return datetime.datetime.strptime(fecha_string, settings.DATE_INPUT_FORMATS[0]).date()

def get_month(fecha_mes):
    return datetime.datetime.strptime(fecha_mes, settings.MONTH_INPUT_FORMATS[0]).date()

def finanzas(request):



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
    """
    cursor = connection.cursor()
    cursor.execute(query, { 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin })
    resultados = dictfetch(cursor, 100, 0)

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
    return render(request, "finanzas.html", context)