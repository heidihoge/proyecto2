from django import forms
from django.forms import DateField

from proyecto2 import settings
from .models import Asistencia


class AsistenciaForm(forms.ModelForm):
    fecha = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Asistencia
        fields = ['id_alumno', 'id_grupo', 'fecha']
