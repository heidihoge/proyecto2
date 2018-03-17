from django import forms

from .models import Grupo


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['id_clase', 'id_profesor', 'cupo_maximo', 'costo']
