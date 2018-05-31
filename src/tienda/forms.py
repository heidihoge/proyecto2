from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms import DateField

from main.forms import CustomModelChoiceField
from proyecto2 import settings
from .models import Factura, Producto, CompraCabecera, CompraDetalle, VentaCabecera, VentaDetalle, \
    Cliente


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




class FomularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_razon', 'ruc_cliente','direccion','telefono']

# #Formulario Producto
class FomularioProducto(forms.ModelForm):
    existencia = forms.IntegerField( initial=0)
    iva = forms.ChoiceField(
        choices=Producto.IVA,
        widget=forms.RadioSelect(choices=Producto.IVA)
    )
    estado = forms.ChoiceField(
        choices=Producto.ESTADO,
        widget=forms.RadioSelect(choices=Producto.ESTADO),
        initial = 'A'
    )
    control_stock = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required = False
    )
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'foto_producto', 'descripcion', 'control_stock', 'precio_venta', 'costo',
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


#Formulario Venta Cabecera
class FormularioVenta(forms.ModelForm):

    monto_total = forms.IntegerField(initial=0)
    total_iva = forms.IntegerField(initial=0)
    total_iva_5 = forms.IntegerField(initial=0)
    total_iva_10 = forms.IntegerField(initial=0)
    total_exentas = forms.IntegerField(initial=0)
    tipo_pago = forms.ChoiceField(
        choices=CompraCabecera.TIPO_PAGO,
        widget=forms.RadioSelect(choices=CompraCabecera.TIPO_PAGO)
    )
    cliente = CustomModelChoiceField(
        label='Ruc Cliente',
        queryset=Cliente.objects.all(),
        widget=autocomplete.ModelSelect2(url='cliente-autocomplete',
                                         attrs={'data-tags': 'true', 'data-language': 'es'}),
    )
    talonario_factura = CustomModelChoiceField(
        queryset=Factura.objects.all(),
        widget=autocomplete.ModelSelect2(url='factura-autocomplete',
                                         attrs={'data-language': 'es'})
    )
    class Meta:
        model = VentaCabecera

        fields = ['talonario_factura', 'cliente', 'fecha','tipo_pago', 'monto_total',
                  'nro_factura', 'nro_factura_punto_emision', 'nro_factura_numero',
                  'total_iva_5','total_iva_10', 'total_iva', 'total_exentas']

class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_razon', 'ruc_cliente', 'direccion', 'telefono']

class FormularioVentaDetalle(forms.ModelForm):
    cantidad = forms.IntegerField(initial=1)
    producto = CustomModelChoiceField(
        queryset=Producto.objects.all(),
        widget=autocomplete.ModelSelect2(url='producto-autocomplete',
                                         attrs={'data-language': 'es'})
    )
    monto_5 = forms.IntegerField(initial=0)
    monto_10 = forms.IntegerField(initial=0)
    monto_exento = forms.IntegerField(initial=0)

    def clean_producto(self):
        if isinstance(self.cleaned_data['producto'], str):
            return Producto.objects.get(codigo='CUENTA')

        return self.cleaned_data['producto']

    class Meta:
        model = VentaDetalle

        fields = ['producto', 'cantidad', 'precio', 'monto_5', 'monto_10', 'monto_exento']



