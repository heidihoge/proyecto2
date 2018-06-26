from django.urls import path

from reportes.views import balance, asistencia, compra, venta

urlpatterns = [
    path('balance', balance, name='balance'),
    path('asistencia', asistencia, name='asistencia'),
    path('compra', compra, name='compra'),
    path('venta', venta, name='venta'),
]

