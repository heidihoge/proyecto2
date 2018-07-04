from django.urls import path

from reportes.views import balance, asistencia, compra, venta, alumnos_por_grupo, list_pagos_fechas, export_tarjeta_csv

urlpatterns = [
    path('balance', balance, name='balance'),
    path('asistencia', asistencia, name='asistencia'),
    path('compra', compra, name='compra'),
    path('venta', venta, name='venta'),
    path('pagos/tarjetas', list_pagos_fechas, name='list_pagos_fechas'),
    path('pagos/tarjetas/export_tarjeta_csv', export_tarjeta_csv, name='export_tarjeta_csv'),
    path('venta', venta, name='venta'),
    path('grupo/alumnos', alumnos_por_grupo, name='alumnos_por_grupo'),
]

