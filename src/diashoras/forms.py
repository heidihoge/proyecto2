from django import forms

from diashoras.models import DiaHora


class DiaHoraForm(forms.ModelForm):
    class Meta:
        model = DiaHora
        fields = ['id_grupo', 'dia', 'hora']
