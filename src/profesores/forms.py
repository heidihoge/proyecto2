from django import forms
from django.forms import DateField

from proyecto2 import settings
from .models import Profesor


class ProfesorForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Profesor
        fields = ['cedula','nombre','apellido','direccion','telefono','fecha_nacimiento','especialidad','salario', 'imagen','ficha']


