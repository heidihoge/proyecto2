from django import forms
from .models import Alumno


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['cedula','nombre','apellido','direccion','telefono','imagen','ficha']


