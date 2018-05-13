from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms import DateField


from proyecto2 import settings
from .models import Factura, Producto, CategoriaProducto, CompraCabecera, CompraDetalle


# ,Timbrado,CategoriaProducto,Producto,Existencia,TipoPago,
# CompraCabecera,CompraDetalle,VentaCabecera,VentaDetalle,Pagos


# Formulario factura
class FomularioFactura(forms.ModelForm):
    estado = forms.ChoiceField(
        choices=Factura.ESTADO,
        widget=forms.RadioSelect(choices=Factura.ESTADO),
        initial = 'A'
    )
    class Meta:
        model = Factura
        fields = ['nombre', 'ruc', 'actividad_economica', 'direccion', 'telefono', 'numero_timbrado', 'punto_emision',
                  'nro_inicial', 'nro_final', 'vigencia_desde', 'vigencia_hasta', 'estado']


# #Formulario CategoriaProducto
# class FomularioCategoriaProducto(forms.ModelForm):
#     class Meta:
#         model = CategoriaProducto
#         fields = ['', '', '', '', '', '', '', '', '', '']
#
# #Formulario CategoriaProducto
class FomularioCategoriaProducto(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ['nombre', 'descripcion']


#
# #Formulario Producto
class FomularioProducto(forms.ModelForm):
    existencia = forms.IntegerField(disabled=True, initial=0)
    iva = forms.ChoiceField(
        choices=Producto.IVA,
        widget=forms.RadioSelect(choices=Producto.IVA)
    )
    estado = forms.ChoiceField(
        choices=Producto.ESTADO,
        widget=forms.RadioSelect(choices=Producto.ESTADO),
        initial = 'A'
    )
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'foto_producto', 'descripcion', 'categoria', 'precio_venta', 'costo',
                  'iva', 'estado', 'existencia']



#Formulario CompraCabecera
class FormularioCompra(forms.ModelForm):

    monto_total = forms.IntegerField(disabled=True, initial=0)
    total_iva = forms.IntegerField(disabled=True, initial=0)
    tipo_pago = forms.ChoiceField(
        choices=CompraCabecera.TIPO_PAGO,
        widget=forms.RadioSelect(choices=CompraCabecera.TIPO_PAGO)
    )
    class Meta:
        model = CompraCabecera

        fields = ['descripcion', 'proveedor', 'fecha','tipo_pago', 'monto_total',
                  'nro_factura','total_iva_5','total_iva_10', 'total_iva']

class FormularioCompraDetalle(forms.ModelForm):
    cantidad = forms.IntegerField(initial=1)
    class Meta:
        model = CompraDetalle

        fields = ['producto', 'cantidad', 'precio']



# #Formulario VentaCabecera
# class FormularioVentaCabecera(forms.ModelForm):
#     class Meta:
#         model = VentaCabecera
#         fields = ['', '', '', '', '', '', '', '', '', '']
#
# #Formulario VentaDetalle
# class FormularioVentaDetalle(forms.ModelForm):
#     class Meta:
#         model = VentaDetalle
#         fields = ['', '', '', '', '', '', '', '', '', '']
#
#
# #Formulario Pagos
#
# class FormularioPago(forms.ModelForm):
#     class Meta:
#         model = Pagos
#         fields = ['', '', '', '', '', '', '', '', '', '']
