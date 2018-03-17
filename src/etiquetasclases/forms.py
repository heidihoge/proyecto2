from django import forms

from etiquetas.models import Etiqueta


class EtiquetaGrupoForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['id_grupo', 'id_etiqueta']
