from django import forms
from django.forms import DateField

from inscripciones.models import Inscripcion
from proyecto2 import settings


class InscripcionForm(forms.ModelForm):
    fecha_inicio = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    fecha_fin = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Inscripcion
        fields = ['id_grupo', 'id_alumno', 'fecha_inicio', 'fecha_fin']
