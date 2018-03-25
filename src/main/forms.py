from django import forms
from django.forms import DateField

from proyecto2 import settings
from .models import Persona, Alumno, Empleado, Profesor, Cuenta, Titular


#Formulario Persona
class PersonaForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Persona
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula']


#Formulario Titular

class TitularForm(forms.ModelForm):
    class Meta:
        model = Titular
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','tipo_responsable']



#Formulario Alumno
class AlumnoForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)

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

