from django.urls import path

from reportes.views import balance

urlpatterns = [
    path('balance', balance, name='balance'),
]

