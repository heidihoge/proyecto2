from django.urls import path

from reportes.views import balance, asistencia, compra, venta, alumnos_por_grupo, list_pagos_fechas

urlpatterns = [
    path('balance', balance, name='balance'),
    path('asistencia', asistencia, name='asistencia'),
    path('compra', compra, name='compra'),
    path('venta', venta, name='venta'),
    path('pagos/fechas', list_pagos_fechas, name='list_pagos_fechas'),
    path('venta', venta, name='venta'),
    path('grupo/alumnos', alumnos_por_grupo, name='alumnos_por_grupo'),
]

