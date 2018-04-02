from dal import autocomplete
from django import forms
from django.forms import DateField

from proyecto2 import settings
from .models import Persona, Alumno, Empleado, Profesor, Cuenta, Titular
from django.core.validators import MinLengthValidator

class CustomModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        return forms.ChoiceField.to_python(self, value)


#Formulario Persona
class PersonaForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    cedula = CustomModelChoiceField(
        queryset=Persona.objects.all(),
        widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'data-tags': 'true', 'data-language':'es'})
    )
    class Meta:
        model = Persona
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula']


#Formulario Titular

class TitularForm(forms.ModelForm):
    cedula = CustomModelChoiceField(
        queryset=Persona.objects.all(),
        widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'data-tags': 'true', 'data-language':'es'}),
    )
    tipo_responsable = forms.ChoiceField(choices=Titular.OPCIONES_TIPO_TUTOR)
    tipo_responsable.widget.attrs = {'class': 'form-control'}
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Titular
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','tipo_responsable']



#Formulario Alumno
class AlumnoForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    cedula = CustomModelChoiceField(
        queryset=Persona.objects.all(),
        widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'data-tags': 'true', 'data-language':'es'})
    )
    class Meta:
        model = Alumno
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','imagen','ficha','ficha_inscripcion','titular_cuenta']



#Formulario Empleado
class EmpleadoForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Empleado
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','salario']


#Formulario Profesor
class ProfesorForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Profesor
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','salario','especialidad']


#Formulario Cuenta
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['descripcion','monto','saldo','id_persona']

