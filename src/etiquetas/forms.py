from django import forms

from etiquetas.models import Etiqueta


class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'descripcion', 'color']
