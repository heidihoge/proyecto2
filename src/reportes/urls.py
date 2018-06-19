from django.urls import path

from reportes.views import finanzas

urlpatterns = [
    path('finanzas', finanzas, name='finanzas'),
]

