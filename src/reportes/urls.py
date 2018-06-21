from django.urls import path

from reportes.views import balance, asistencia

urlpatterns = [
    path('balance', balance, name='balance'),
    path('asistencia', asistencia, name='asistencia'),
]

