from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateField

from proyecto2 import settings
from .models import Persona, Alumno, Empleado, Profesor, Cuenta, Titular
from django.core.validators import MinLengthValidator

class CustomModelChoiceField(forms.ModelChoiceField):
    def __init__(self, model=None, allow_create=False, **kwargs):
        forms.ModelChoiceField.__init__(self, **kwargs)
        self.allow_create = allow_create
        self.model = model


    def to_python(self, value):
        try:
            return super(CustomModelChoiceField, self).to_python(forms.ChoiceField.to_python(self, value))
        except ValidationError as err:
            # Esto permite crear un objeto nuevo si no existe
            if err.code == 'invalid_choice' and self.allow_create and self.model is not None:
                key = self.to_field_name or 'pk'
                return self.model(**{key: value})



#Formulario Persona
class PersonaForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    direccion = forms.CharField(label='Dirección')
    telefono1 = forms.CharField(label='Teléfono')
    telefono2 = forms.CharField(label='Otro contacto')
    cedula = CustomModelChoiceField(
        queryset=Persona.objects.all(),
        widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'data-tags': 'true', 'data-language':'es'})
    )
    sexo = forms.ChoiceField(
        choices=Persona.SEXO,
        widget=forms.RadioSelect(choices=Persona.SEXO)
    )
    estado = forms.ChoiceField(
        choices=Persona.ESTADO,
        widget=forms.RadioSelect(choices=Persona.ESTADO),
        initial='A'
    )
    class Meta:
        model = Persona
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','estado']


#Formulario Titular

class TitularForm(forms.ModelForm):
    direccion = forms.CharField(label='Dirección')
    telefono1 = forms.CharField(label='Teléfono')
    telefono2 = forms.CharField(label='Otro contacto')
    cedula = CustomModelChoiceField(
        to_field_name='cedula',
        model=Persona,
        allow_create=True,
        # Se ejecuta cuando se quiere guardar el form y verificar que exista en la base de datos.
        queryset=Persona.objects.all().values_list('cedula', flat=True),
        widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'data-tags': 'true', 'data-language':'es'}),
    )
    sexo = forms.ChoiceField(
        choices=Persona.SEXO,
        widget=forms.RadioSelect(choices=Persona.SEXO)
    )
    estado = forms.ChoiceField(
        choices=Persona.ESTADO,
        widget=forms.RadioSelect(choices=Persona.ESTADO),
        initial='A'
    )
    tipo_responsable = forms.ChoiceField(choices=Titular.OPCIONES_TIPO_TUTOR)
    tipo_responsable.widget.attrs = {'class': 'form-control'}
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Titular
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','tipo_responsable','estado']


#Formulario Alumno
class AlumnoForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    direccion = forms.CharField(label='Dirección')
    telefono1 = forms.CharField(label='Teléfono')
    telefono2 = forms.CharField(label='Otro contacto')
    cedula = CustomModelChoiceField(
        to_field_name='cedula',
        model=Persona,
        allow_create=True,
        # Se ejecuta cuando se quiere guardar el form y verificar que exista en la base de datos.
        queryset=Persona.objects.all().values_list('cedula', flat=True),
        widget=autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'data-tags': 'true', 'data-language':'es'})
    )
    sexo = forms.ChoiceField(
        choices=Persona.SEXO,
        widget=forms.RadioSelect(choices=Persona.SEXO)
    )
    estado = forms.ChoiceField(
        choices=Persona.ESTADO,
        widget=forms.RadioSelect(choices=Persona.ESTADO),
        initial='A'
    )
    class Meta:
        model = Alumno

        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','imagen','ficha','ficha_inscripcion','estado']


#Formulario Empleado
class EmpleadoForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    direccion = forms.CharField(label='Dirección')
    telefono1 = forms.CharField(label='Teléfono')
    telefono2 = forms.CharField(label='Otro contacto')
    sexo = forms.ChoiceField(
        choices=Persona.SEXO,
        widget=forms.RadioSelect(choices=Persona.SEXO)
    )

    estado = forms.ChoiceField(
        choices=Persona.ESTADO,
        widget=forms.RadioSelect(choices=Persona.ESTADO)
    )

    class Meta:
        model = Empleado
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','salario','rol']




#Formulario Profesor
class ProfesorForm(forms.ModelForm):
    fecha_nacimiento = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    direccion = forms.CharField(label='Dirección')
    telefono1 = forms.CharField(label='Teléfono')
    telefono2 = forms.CharField(label='Otro contacto')

    class Meta:
        model = Profesor
        fields = ['cedula','nombre','apellido','fecha_nacimiento','sexo','direccion','telefono1','telefono2','fotocopia_cedula','salario','especialidad']

    sexo = forms.ChoiceField(
        choices=Persona.SEXO,
        widget=forms.RadioSelect(choices=Persona.SEXO)
    )


#Formulario Cuenta
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['descripcion','monto','saldo','id_persona']

