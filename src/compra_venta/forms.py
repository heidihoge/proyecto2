from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms import DateField

from escuela import admin
from main.models import Profesor
from proyecto2 import settings
from .models import TipoDocumento,Timbrado,CategoriaProducto,Producto,Existencia,TipoPago,CompraCabecera,CompraDetalle,VentaCabecera,VentaDetalle,Pagos



#Formulario TipoDocumento
class FomularioDocumento(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = ['','','','','','','','','','']

#Formulario Timbrado
class FomularioTimbrado(forms.ModelForm):
    class Meta:
        model = Timbrado
        fields = ['','','','','','','','','','']

#Formulario CategoriaProducto
class FomularioCategoriaProducto(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ['', '', '', '', '', '', '', '', '', '']

#Formulario Producto
class FomularioProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['', '', '', '', '', '', '', '', '', '']

#Formulario Existencia
class FormularioExistencia(forms.ModelForm):
    class Meta:
        model = Existencia
        fields = ['', '', '', '', '', '', '', '', '', '']

#Formulario TipoPago
class FormularioTipoPago(forms.ModelForm):
    class Meta:
        model = TipoPago
        fields = ['', '', '', '', '', '', '', '', '', '']

#Formulario CompraCabecera
class FormularioCompraCabecera(forms.ModelForm):
    class Meta:
        model = CompraCabecera
        fields = ['', '', '', '', '', '', '', '', '', '']


#Formulario CompraDetalle
class FormularioCompraDetalle(forms.ModelForm):
    class Meta:
        model = CompraDetalle
        fields = ['', '', '', '', '', '', '', '', '', '']

#Formulario VentaCabecera
class FormularioVentaCabecera(forms.ModelForm):
    class Meta:
        model = VentaCabecera
        fields = ['', '', '', '', '', '', '', '', '', '']

#Formulario VentaDetalle
class FormularioVentaDetalle(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ['', '', '', '', '', '', '', '', '', '']


#Formulario Pagos

class FormularioPago(forms.ModelForm):
    class Meta:
        model = Pagos
        fields = ['', '', '', '', '', '', '', '', '', '']