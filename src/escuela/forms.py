from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms import DateField

from escuela import admin
from proyecto2 import settings
from .models import Clase, Grupo, DiaHora, Etiqueta, EtiquetaClase, EtiquetaGrupo,Inscripcion,Asistencia


#Formulario Clase
class FomularioClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre','descripcion','costo']

#Formulario Grupo

class FomularioGrupo(forms.ModelForm):
    id_clase = forms.ModelChoiceField(queryset=Clase.objects.all())

    def __init__(self, *args, **kwargs):
        super(FomularioGrupo, self).__init__(*args, **kwargs)
        clase_rel = ManyToOneRel(Grupo.id_clase, Clase, 'id')
        self.fields['id_clase'].widget = RelatedFieldWidgetWrapper(self.fields['id_clase'].widget, clase_rel, admin.admin.site)
    class Meta:
        model = Grupo
        fields = ['id_clase', 'id_profesor', 'cupo_maximo','costo']


#Formulario DiaHora
class FomularioDiaHora(forms.ModelForm):
    class Meta:
        model = DiaHora
        fields = ['id_grupo', 'dia', 'hora']

#Formulario Etiqueta
class FomularioEtiqueta(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'descripcion', 'color']


#Formulario EtiquetaClase
class FomularioEtiquetaClase(forms.ModelForm):
    class Meta:
        model = EtiquetaClase
        fields = ['id_clase', 'etiqueta']

#Formulario EtiquetaGrupo
class FomularioEtiquetaGrupo(forms.ModelForm):
    class Meta:
        model = EtiquetaGrupo
        fields = ['id_grupo', 'etiqueta']

#Formulario Inscripcion
class FomularioInscripcion(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['id_grupo', 'id_alumno','fecha_inicio','fecha_fin']

#Formulario Asistencia
class FomularioAsistencia(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['id_alumno','id_grupo', 'fecha']

