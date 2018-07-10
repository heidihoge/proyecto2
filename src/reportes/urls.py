from django.urls import path

from reportes.views import balance, asistencia, compra, venta, alumnos_por_grupo, list_pagos_tarjeta_fechas, \
    export_tarjeta_csv, \
    list_pagos_cheque_fechas, export_cheque_csv, balance_anio, enviar_mail_balance

urlpatterns = [
    path('balance', balance, name='balance'),
    path('balance_anio', balance_anio, name='balance_anio'),
    path('asistencia', asistencia, name='asistencia'),
    path('compra', compra, name='compra'),
    path('venta', venta, name='venta'),
    path('pagos/tarjetas', list_pagos_tarjeta_fechas, name='list_pagos_tarjeta_fechas'),
    path('pagos/cheques', list_pagos_cheque_fechas, name='list_pagos_cheques_fechas'),
    path('venta', venta, name='venta'),
    path('grupo/alumnos', alumnos_por_grupo, name='alumnos_por_grupo'),
    path('mail_balance', enviar_mail_balance, name='mail_balance'),
]

