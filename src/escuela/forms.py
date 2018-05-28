
from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms import DateField

from escuela import admin
from main.forms import CustomModelChoiceField
from main.models import Profesor, Alumno, Persona
from proyecto2 import settings
from .models import Clase, Grupo,  Etiqueta, EtiquetaClase, EtiquetaGrupo,Inscripcion,Asistencia


#Formulario Clase
class FormularioClase(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre','descripcion','costo']

#Formulario Grupo
class FormularioGrupo(forms.ModelForm):

    class Meta:
        model = Grupo
        fields = ['id_clase', 'id_profesor', 'cupo_maximo', 'costo', 'hora_inicio', 'hora_fin', 'lunes', 'martes',
                  'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

    id_clase = forms.ModelChoiceField(
        queryset=Clase.objects.all(),
        widget=autocomplete.ModelSelect2(url='clases-autocomplete'),
        label='Clase'
    )
    id_profesor = forms.ModelChoiceField(
        queryset=Profesor.objects.all(),
        widget=autocomplete.ModelSelect2(url='profesor-autocomplete'),
        label = 'Profesor'
    )
    hora_inicio = forms.Field(
        widget=forms.TextInput(attrs={'class': 'clock form-control'})
    )
    hora_fin = forms.Field(
        widget=forms.TextInput(attrs={'class': 'clock form-control'})
    )
    lunes = forms.Field(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
    )
    martes = forms.Field(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
    )
    miercoles = forms.Field(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
    )
    jueves = forms.Field(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
    )
    viernes = forms.Field(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
    )
    sabado = forms.Field(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
    )
    domingo = forms.Field(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
    )

# # #Formulario DiaHora
# # class FomularioDiaHora(forms.ModelForm):
# #     grupo_id = CustomModelChoiceField(
# #         queryset=Grupo.objects.all(),
# #         widget=autocomplete.ModelSelect2(url='grupo-autocomplete', attrs={'data-language': 'es'})
# #     )
#     hora_inicio = forms.Field(
#         widget=forms.TextInput(attrs={'class': 'clock form-control'})
#     )
#     hora_fin = forms.Field(
#         widget=forms.TextInput(attrs={'class': 'clock form-control'})
#     )
#     lunes = forms.Field(
#         required=False,
#         initial=False,
#         widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
#     )
#     martes = forms.Field(
#         required=False,
#         initial=False,
#         widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
#     )
#     miercoles = forms.Field(
#         required=False,
#         initial=False,
#         widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
#     )
#     jueves = forms.Field(
#         required=False,
#         initial=False,
#         widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
#     )
#     viernes = forms.Field(
#         required=False,
#         initial=False,
#         widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
#     )
#     sabado = forms.Field(
#         required=False,
#         initial=False,
#         widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
#     )
#     domingo = forms.Field(
#         required=False,
#         initial=False,
#         widget=forms.CheckboxInput(attrs={'class': 'flat-only'})
#     )
#
#
#
#     class Meta:
#         model = DiaHora
#         fields = ['grupo_id', 'hora_inicio', 'hora_fin', 'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
#

#Formulario Etiqueta
class FomularioEtiqueta(forms.ModelForm):
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'with-colorpicker'}))
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'descripcion', 'color']


#Formulario EtiquetaClase
class FomularioEtiquetaClase(forms.ModelForm):
    class Meta:
        model = EtiquetaClase
        fields = ['id_clase', 'etiqueta']

#Formulario EtiquetaGrupo
class FormularioEtiquetaGrupo(forms.ModelForm):
    class Meta:
        model = EtiquetaGrupo
        fields = ["grupo", 'etiqueta']

#Formulario Inscripcion
class FormularioInscripcion(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        widget=autocomplete.ModelSelect2(url='grupo-autocomplete'),
        label='Grupo'
    )
    fecha_inicio = DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Inscripcion
        fields = ["grupo", 'fecha_inicio']

#Formulario Asistencia
class FormularioAsistencia(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['id_alumno', "grupo", 'fecha']

