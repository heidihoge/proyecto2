from django import forms
from django.forms import DateField

from proyecto2 import settings
from .models import Persona


class PersonaForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Persona
        fields = ['cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'direccion', 'telefono1', 'telefono2',
                  'fotocopia_cedula']
