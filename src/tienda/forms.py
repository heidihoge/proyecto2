from dal import autocomplete
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.forms import DateField

from main.forms import CustomModelChoiceField
from main.utils import CurrencyIntegerField
from proyecto2 import settings
from .models import Factura, Producto, CompraCabecera, CompraDetalle, VentaCabecera, VentaDetalle, \
    Cliente, OperacionCaja, Pago, Recibo


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

    def __init__(self, *args, **kwargs):
        super(FomularioFactura, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = 'Nombre de la Escuela'
        self.fields['ruc'].widget.attrs['placeholder'] = 'RUC de la Escuela'
        self.fields['actividad_economica'].widget.attrs['placeholder'] = 'Educación'
        self.fields['direccion'].widget.attrs['placeholder'] = 'Dirección de la escuela'
        self.fields['telefono'].widget.attrs['placeholder'] = 'Teléfono de la escuela'
        self.fields['punto_emision'].widget.attrs['placeholder'] = '001-001'

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
        self.fields['codigo'].widget.attrs['placeholder'] = 'Codigo de producto. Ej: VEST001.'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Nombre del producto. Ej: Malla.'
        self.fields['descripcion'].widget.attrs['placeholder'] = 'Descripción del producto, color, marca y tamaño.'
        self.fields['precio_venta'].widget.attrs['placeholder'] = 'Precio de venta, el cuál debe ser mayor al precio de compra. Ej: 120.000GS.'
        self.fields['costo'].widget.attrs['placeholder'] = 'Precio de adquisión del producto, el cuál es menor al precio de venta. Ej: 100.000GS.'

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
    credito_plazo = forms.IntegerField(initial=0)

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

        fields = ['talonario_factura', 'cliente', 'fecha', 'tipo_pago', 'credito_plazo', 'monto_total',
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
    credito_plazo = forms.IntegerField(initial=0, required=False)

    class Meta:
        model = VentaCabecera

        fields = ['talonario_factura', 'cliente', 'fecha', 'tipo_pago', 'credito_plazo', 'monto_total', 'credito_plazo',
                  'nro_factura', 'nro_factura_punto_emision', 'nro_factura_numero',
                  'total_iva_5', 'total_iva_10', 'total_grav_5', 'total_grav_10', 'total_grav_exentas', 'total_iva']
        exclude = ["cliente"]

    def clean(self):
        cleaned_data = super().clean()

        tipo_pago = cleaned_data.get("tipo_pago")

        if tipo_pago == 'Crédito':
            credito_plazo = cleaned_data.get("credito_plazo")
            if type(credito_plazo) != int or credito_plazo < 1:
                self.add_error('credito_plazo', 'El plazo debe ser mayor a 0.')



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

class FormularioReciboTarjeta(forms.ModelForm):
    class Meta:
        model = Recibo
        fields = ['tarjeta', 'nro_autorizacion', 'ultimos_tarjeta']

    def __init__(self, *args, **kwargs):
        super(FormularioReciboTarjeta, self).__init__(*args, **kwargs)
        self.fields['tarjeta'].required = True
        self.fields['nro_autorizacion'].required = True
        self.fields['ultimos_tarjeta'].required = True

class FormularioReciboCheque(forms.ModelForm):
    class Meta:
        model = Recibo
        fields = ['banco', 'nro_cuenta', 'librador', 'serie_cheque',
                  'nro_cheque', 'fecha_emision', 'fecha_venc']

    def __init__(self, *args, **kwargs):
        super(FormularioReciboCheque, self).__init__(*args, **kwargs)
        self.fields['banco'].required = True
        self.fields['nro_cuenta'].required = True
        self.fields['librador'].required = True
        self.fields['serie_cheque'].required = True
        self.fields['nro_cheque'].required = True
        self.fields['fecha_emision'].required = True
        self.fields['fecha_venc'].required = True

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
        self.fields['ultimos_tarjeta'].widget.attrs['placeholder'] = '4 Últimos Dígito de Tarjeta'
        self.fields['nro_autorizacion'].widget.attrs['placeholder'] = 'Nro Autorización Pago'
        self.fields['banco'].widget.attrs['placeholder'] = 'Nombre del Banco Emisor'
        self.fields['librador'].widget.attrs['placeholder'] = 'Nombre de Cliente'
        self.fields['nro_cuenta'].widget.attrs['placeholder'] = 'Nro. Cuenta Bancaria'
        self.fields['nro_cheque'].widget.attrs['placeholder'] = 'Nro. Cheque'
        self.fields['serie_cheque'].widget.attrs['placeholder'] = 'Nro. de Serie del Cheque'



    monto = CurrencyIntegerField(initial=0, label="Monto Total")
    monto_efectivo = CurrencyIntegerField(initial=0)
    monto_efectivo_abonado = CurrencyIntegerField(initial=0)
    monto_efectivo_vuelto = CurrencyIntegerField(initial=0)
    monto_tarjeta = CurrencyIntegerField(initial=0)
    monto_cheque = CurrencyIntegerField(initial=0)
    pago_efectivo = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'flat'}), required=False)
    pago_tarjeta = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'flat'}), required=False)
    pago_cheque = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'flat'}), required=False)
    tarjeta = forms.CharField(required=False)
    nro_autorizacion = forms.CharField(required=False)
    ultimos_tarjeta = forms.CharField(required=False)
    nro_cuenta = forms.CharField(required=False)
    librador = forms.CharField(required=False)
    serie_cheque = forms.CharField(required=False)
    nro_cheque = forms.CharField(required=False)
    fecha_emision = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    fecha_venc = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)

class FormularioRecibo(forms.ModelForm):
    class Meta:
        model = Recibo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormularioRecibo, self).__init__(*args, **kwargs)
        self.fields['ultimos_tarjeta'].widget.attrs['placeholder'] = '4 Últimos Dígito de Tarjeta'
        self.fields['nro_autorizacion'].widget.attrs['placeholder'] = 'Nro Autorización Pago'
        self.fields['banco'].widget.attrs['placeholder'] = 'Nombre del Banco Emisor'
        self.fields['librador'].widget.attrs['placeholder'] = 'Nombre de Cliente'
        self.fields['nro_cuenta'].widget.attrs['placeholder'] = 'Nro. Cuenta Bancaria'
        self.fields['nro_cheque'].widget.attrs['placeholder'] = 'Nro. Cheque'
        self.fields['serie_cheque'].widget.attrs['placeholder'] = 'Nro. de Serie del Cheque'

    monto = CurrencyIntegerField(initial=0, label="Monto Recibo")
    monto_efectivo = CurrencyIntegerField(initial=0)
    monto_efectivo_abonado = CurrencyIntegerField(initial=0)
    monto_efectivo_vuelto = CurrencyIntegerField(initial=0)
    monto_tarjeta = CurrencyIntegerField(initial=0)
    monto_cheque = CurrencyIntegerField(initial=0)
    pago_efectivo = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'flat'}), required=False)
    pago_tarjeta = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'flat'}), required=False)
    pago_cheque = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'flat'}), required=False)
    nombre_cliente = forms.CharField(required=False)
    tarjeta = forms.CharField(required=False)
    nro_autorizacion = forms.CharField(required=False)
    ultimos_tarjeta = forms.CharField(required=False)
    nro_cuenta = forms.CharField(required=False)
    librador = forms.CharField(required=False)
    serie_cheque = forms.CharField(required=False)
    nro_cheque = forms.CharField(required=False)
    fecha = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    fecha_emision = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    fecha_venc = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)


class FormularioOperacionCaja(forms.ModelForm):
    monto = CurrencyIntegerField()
    class Meta:
        model = OperacionCaja
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormularioOperacionCaja, self).__init__(*args, **kwargs)
        self.fields['concepto'].widget.attrs['placeholder'] = 'Gastos o entrada de dinero para caja chica. Ej: Gastos Varios'
        self.fields['descripcion'].widget.attrs['placeholder'] = 'Breve descripción del gasto'
        self.fields['monto'].widget.attrs['placeholder'] = 'Monto del gasto realizado'


    tipo_transaccion = forms.ChoiceField(
        choices=OperacionCaja.TIPO_TRANSACCION,
        widget=forms.RadioSelect(choices=OperacionCaja.TIPO_TRANSACCION),
        initial='A'
    )



class FormularioReporteCompras(forms.ModelForm):
    class Meta:
        model = CompraCabecera
        fields = ['fecha', 'nro_factura','ruc_proveedor','proveedor','monto_total' ]

