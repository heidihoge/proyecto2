from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms import DateField

from main.forms import CustomModelChoiceField
from main.utils import CurrencyIntegerField
from proyecto2 import settings
from .models import Factura, Producto, CompraCabecera, CompraDetalle, VentaCabecera, VentaDetalle, \
    Cliente, OperacionCaja, Pago


# ,Timbrado,CategoriaProducto,Producto,Existencia,TipoPago,
# CompraCabecera,CompraDetalle,VentaCabecera,VentaDetalle,Pagos

# Formulario factura
class FomularioFactura(forms.ModelForm):
    estado = forms.ChoiceField(
        choices=Factura.ESTADO,
        widget=forms.RadioSelect(choices=Factura.ESTADO),
        initial='A'
    )

    class Meta:
        model = Factura
        fields = ['nombre', 'ruc', 'actividad_economica', 'direccion', 'telefono', 'numero_timbrado', 'punto_emision',
                  'nro_inicial', 'nro_final', 'vigencia_desde', 'vigencia_hasta', 'estado']


# #Formulario Producto
class FomularioProducto(forms.ModelForm):
    existencia = forms.IntegerField(initial=0)
    iva = forms.ChoiceField(
        choices=Producto.IVA,
        widget=forms.RadioSelect(choices=Producto.IVA)
    )
    estado = forms.ChoiceField(
        choices=Producto.ESTADO,
        widget=forms.RadioSelect(choices=Producto.ESTADO),
        initial='A'
    )
    control_stock = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False
    )
    precio_venta = CurrencyIntegerField()
    costo = CurrencyIntegerField()

    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'foto_producto', 'descripcion', 'control_stock', 'precio_venta', 'costo',
                  'iva', 'estado', 'existencia']

    def __init__(self, *args, **kwargs):
        super(FomularioProducto, self).__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['placeholder'] = 'Cédula del titular'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Cédula del titular'
        self.fields['descripcion'].widget.attrs['placeholder'] = 'Nombre completo del titular'


# Formulario CompraCabecera
class FormularioCompra(forms.ModelForm):
    def clean_monto_total(self):
        monto = self.cleaned_data['monto_total']
        if monto == 0:
            raise forms.ValidationError("El monto es 0! Verifica los detalles.")
        if monto < 0:
            raise forms.ValidationError("El monto es negativo! Verifica los detalles.")
        return monto

    monto_total = CurrencyIntegerField(initial=0)
    total_iva = CurrencyIntegerField(initial=0)
    total_iva_5 = CurrencyIntegerField(initial=0)
    total_iva_10 = CurrencyIntegerField(initial=0)
    total_grav_5 = CurrencyIntegerField(initial=0)
    total_grav_10 = CurrencyIntegerField(initial=0)
    total_grav_exentas = CurrencyIntegerField(initial=0)

    tipo_pago = forms.ChoiceField(
        choices=CompraCabecera.TIPO_PAGO,
        widget=forms.RadioSelect(choices=CompraCabecera.TIPO_PAGO)
    )

    class Meta:
        model = CompraCabecera

        fields = ['descripcion', 'ruc_proveedor','proveedor', 'fecha', 'tipo_pago', 'monto_total',
                  'nro_factura', 'total_iva_5', 'total_iva_10', 'total_iva','total_grav_5','total_grav_10','total_grav_exentas']



class FormularioCompraDetalle(forms.ModelForm):
    monto_5 = CurrencyIntegerField(initial=0)
    monto_10 = CurrencyIntegerField(initial=0)
    monto_exento = CurrencyIntegerField(initial=0)

    class Meta:
        model = CompraDetalle

        fields = '__all__'


# Formulario Venta Cabecera
class FormularioVenta(forms.ModelForm):
    monto_total = forms.IntegerField(initial=0)
    total_iva = forms.IntegerField(initial=0, label="Total IVA")
    total_iva_5 = forms.IntegerField(initial=0, label="Total IVA 5%")
    total_iva_10 = forms.IntegerField(initial=0, label="Total IVA 10%")
    total_grav_5 = forms.IntegerField(initial=0, label="Total IVA 5%")
    total_grav_10 = forms.IntegerField(initial=0, label="Total IVA 10%")
    total_exentas = forms.IntegerField(initial=0)
    tipo_pago = forms.ChoiceField(
        choices=VentaCabecera.TIPO_PAGO,
        widget=forms.RadioSelect(choices=VentaCabecera.TIPO_PAGO),
        label="Condición de venta"
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

        fields = ['talonario_factura', 'cliente', 'fecha', 'tipo_pago', 'monto_total',
                  'nro_factura', 'nro_factura_punto_emision', 'nro_factura_numero',
                  'total_iva_5', 'total_iva_10','total_grav_5', 'total_grav_10', 'total_iva', 'total_grav_exentas']




class FormularioVentaVerificar(forms.ModelForm):

    monto_total = CurrencyIntegerField()
    total_iva_5 = CurrencyIntegerField()
    total_iva_10 = CurrencyIntegerField()
    total_iva = CurrencyIntegerField()
    total_grav_5 = CurrencyIntegerField()
    total_grav_10 = CurrencyIntegerField()
    total_grav_exentas = CurrencyIntegerField()

    class Meta:
        model = VentaCabecera

        fields = ['talonario_factura', 'cliente', 'fecha', 'tipo_pago', 'monto_total',
                  'nro_factura', 'nro_factura_punto_emision', 'nro_factura_numero',
                  'total_iva_5', 'total_iva_10', 'total_grav_5', 'total_grav_10', 'total_grav_exentas', 'total_iva']
        exclude = ["cliente"]


class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_razon', 'ruc_cliente', 'direccion', 'telefono']

    def __init__(self, *args, **kwargs):
        super(FormularioCliente, self).__init__(*args, **kwargs)
        self.fields['nombre_razon'].widget.attrs['placeholder'] = 'Nombre del cliente'
        self.fields['ruc_cliente'].widget.attrs['placeholder'] = 'RUC del cliente'
        self.fields['direccion'].widget.attrs['placeholder'] = 'Dirección del cliente'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Teléfono del cliente'



class FormularioVentaDetalle(forms.ModelForm):
    cantidad = forms.IntegerField(initial=1)
    producto = CustomModelChoiceField(
        queryset=Producto.objects.all(),
        widget=autocomplete.ModelSelect2(url='producto-autocomplete',
                                         attrs={'data-language': 'es'})
    )
    precio = CurrencyIntegerField(initial=0)
    monto_5 = CurrencyIntegerField(initial=0)
    monto_10 = CurrencyIntegerField(initial=0)
    monto_exento = CurrencyIntegerField(initial=0)

    def clean_producto(self):
        if isinstance(self.cleaned_data['producto'], str):
            return Producto.objects.get(codigo='CUENTA')

        return self.cleaned_data['producto']

    class Meta:
        model = VentaDetalle

        fields = ['producto', 'cantidad', 'precio', 'monto_5', 'monto_10', 'monto_exento']


class FormularioPagoTarjeta(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['tarjeta', 'nro_autorizacion', 'ultimos_tarjeta']

    def __init__(self, *args, **kwargs):
        super(FormularioPagoTarjeta, self).__init__(*args, **kwargs)
        self.fields['tarjeta'].required = True
        self.fields['nro_autorizacion'].required = True
        self.fields['ultimos_tarjeta'].required = True

class FormularioPagoCheque(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['banco', 'nro_cuenta', 'librador', 'serie_cheque',
                  'nro_cheque', 'fecha_emision', 'fecha_venc']

    def __init__(self, *args, **kwargs):
        super(FormularioPagoCheque, self).__init__(*args, **kwargs)
        self.fields['banco'].required = True
        self.fields['nro_cuenta'].required = True
        self.fields['librador'].required = True
        self.fields['serie_cheque'].required = True
        self.fields['nro_cheque'].required = True
        self.fields['fecha_emision'].required = True
        self.fields['fecha_venc'].required = True


class FormularioPago(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormularioPago, self).__init__(*args, **kwargs)
        self.fields['ultimos_tarjeta'].widget.attrs['placeholder'] = '4 últimos dígito de tarjeta'
        self.fields['nro_autorizacion'].widget.attrs['placeholder'] = 'Nro Autorización Pago'
        self.fields['banco'].widget.attrs['placeholder'] = 'Nombre del Banco emisor'
        self.fields['librador'].widget.attrs['placeholder'] = 'Nombre de Cliente'
        self.fields['nro_cuenta'].widget.attrs['placeholder'] = 'Nro. cuenta bancaria'
        self.fields['nro_cheque'].widget.attrs['placeholder'] = 'Nro. Cheque'



    monto = CurrencyIntegerField(initial=0)
    tarjeta = forms.CharField(required=False)
    nro_autorizacion = forms.CharField(required=False)
    ultimos_tarjeta = forms.CharField(required=False)
    nro_cuenta = forms.CharField(required=False)
    librador = forms.CharField(required=False)
    serie_cheque = forms.CharField(required=False)
    nro_cheque = forms.CharField(required=False)
    fecha_emision = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    fecha_venc = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)


class FormularioOperacionCaja(forms.ModelForm):
    monto = CurrencyIntegerField()
    class Meta:
        model = OperacionCaja
        fields = '__all__'




    tipo_transaccion = forms.ChoiceField(
        choices=OperacionCaja.TIPO_TRANSACCION,
        widget=forms.RadioSelect(choices=OperacionCaja.TIPO_TRANSACCION),
        initial='A'
    )



class FormularioReporteCompras(forms.ModelForm):
    class Meta:
        model = CompraCabecera
        fields = ['fecha', 'nro_factura','ruc_proveedor','proveedor','monto_total' ]

