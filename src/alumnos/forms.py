from django import forms
from django.forms import DateField

from proyecto2 import settings
from .models import Alumno


class AlumnoForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Alumno
        fields = ['cedula','nombre','apellido','direccion','telefono', 'fecha_nacimiento','imagen','ficha']


