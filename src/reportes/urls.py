from django.urls import path

from reportes.views import balance, asistencia, compra, venta, alumnos_por_grupo

urlpatterns = [
    path('balance', balance, name='balance'),
    path('asistencia', asistencia, name='asistencia'),
    path('compra', compra, name='compra'),
    path('venta', venta, name='venta'),
    path('grupo/alumnos', alumnos_por_grupo, name='alumnos_por_grupo'),
]

