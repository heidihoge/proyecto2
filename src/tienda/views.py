import datetime

import logging
from dal import autocomplete
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.db import transaction, IntegrityError, connection
from django.db.models import Q, Max, Sum
from django.db.models.functions import Coalesce
from django.db.transaction import rollback
from django.forms import inlineformset_factory, BaseFormSet, BaseInlineFormSet
from django.shortcuts import render, redirect
from django.urls import reverse

from escuela.models import Cuenta, Grupo
from escuela.utils import dictfetch
from escuela.views import calcular_fecha
from main.models import Persona
from proyecto2 import settings
from .forms import FomularioFactura, FormularioCompra, FormularioCompraDetalle, FormularioVentaDetalle, FormularioVenta, \
    FormularioCliente, FormularioVentaVerificar, FormularioOperacionCaja, FormularioPago, \
    FormularioReporteCompras, FormularioPagoTarjeta, FormularioPagoCheque

from .forms import  FomularioProducto
from .models import Producto, CompraCabecera, CompraDetalle, VentaCabecera, VentaDetalle, Cliente, OperacionCaja, Pago

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

class FacturaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Factura.objects.none()

        hoy = datetime.datetime.today()

        # Trae solo lo vigente y activo
        qs = Factura.objects.filter(Q(vigencia_desde__lte=hoy) & Q(vigencia_hasta__gte=hoy) & Q(estado='A'))

        if self.q:
            qs = qs.filter(Q(ruc__istartswith=self.q) | Q(numero_timbrado__istartswith=self.q))

        return qs

    def _get_fields_as_json(self, result):
        # return json.loads(serializers.serialize('json', [result]))[0]['fields']
        result = result.__dict__
        del result['_state']
        if isinstance(result['vigencia_desde'], datetime.date):
            result['vigencia_desde'] = result['vigencia_desde'].strftime(settings.DATE_INPUT_FORMATS[0])
        if isinstance(result['vigencia_hasta'], datetime.date):
            result['vigencia_hasta'] = result['vigencia_hasta'].strftime(settings.DATE_INPUT_FORMATS[0])

        result['nro_factura'] = self._numero_factura(result)
        return result

    def _numero_factura(self, factura):
        """
        Funcion para obtener numero de la factura
        :param factura: objeto de tipo Factura
        :return: Siguiente numero de factura
        """
        # Completa con 0s

        maximo = VentaCabecera.objects.aggregate(maximo=Max('nro_factura_numero', filter=Q(talonario_factura_id=factura['id'])))

        siguiente = maximo['maximo'] + 1 if maximo['maximo'] else factura['nro_inicial']

        # el siguiente esta fuera del rango permitido, retorna None
        if factura['nro_inicial'] > siguiente or factura['nro_final'] < siguiente:
            return None

        return "{:07d}".format(siguiente)

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return list(filter(lambda x: x['fields']['nro_factura'] is not None,[
            {
                'id': result.pk,
                'text': self.get_result_label(result),
                'pk': result.pk,
                'fields': self._get_fields_as_json(result)
            } for result in context['object_list']
        ]))

class ProductoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Producto.objects.none()

        # busca producto
        qs = Producto.objects.filter(estado='A').exclude(codigo='CUENTA')


        if self.q:
            qs = qs.filter(Q(nombre__icontains=self.q) | Q(codigo__startswith=self.q))

        return qs.order_by('pk')


    def _get_fields_as_json(self, result):
        # return json.loads(serializers.serialize('json', [result]))[0]['fields']
        result = result.__dict__
        del result['_state']

        def iva_str(iva):
            print("iva", iva)
            if str(iva) == '0.05':
                return "5%"
            elif str(iva) == '0.10':
                return "10%"
            else:
                return "exentas"

        result['iva'] = iva_str(result['iva'])

        return result

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': result.pk,
                'text': self.get_result_label(result),
                'pk': result.pk,
                'fields': self._get_fields_as_json(result)
            } for result in context['object_list']
        ]


class CuentaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Cuenta.objects.none()

        # busca Cuentas sin pagar
        qs = Cuenta.objects.filter(pagado=False)

        # if self.q:
        #     qs = qs.filter(Q(inscripcion__alumno__cedula__istartswith=self.q) |
        #                    Q(inscripcion__alumno__titular_cuenta__cedula__istartswith=self.q))
        #
        # return qs


# al elegir que cuenta pagar poder buscar por nombre apellido o cedula del alumno o del titular

        if self.q:
            qs = qs.filter(Q(inscripcion__alumno__cedula__istartswith=self.q) |
                           Q(inscripcion__alumno__titular_cuenta__cedula__istartswith=self.q) |
                           Q(inscripcion__alumno__titular_cuenta__nombre__istartswith=self.q) |
                           Q(inscripcion__alumno__titular_cuenta__apellido__istartswith=self.q) |
                           Q(inscripcion__alumno__nombre__istartswith=self.q) |
                           Q(inscripcion__alumno__apellido__istartswith=self.q) )

        return qs


    def _get_fields_as_json(self, result):
        # return json.loads(serializers.serialize('json', [result]))[0]['fields']


        result = result.__dict__
        del result['_state']
        if isinstance(result['vencimiento'], datetime.date):
            result['vencimiento'] = result['vencimiento'].strftime(settings.DATE_INPUT_FORMATS[0])
        return result

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': result.pk,
                'text': self.get_result_label(result),
                'pk': result.pk,
                'fields': self._get_fields_as_json(result)
            } for result in context['object_list']
        ]




class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Cliente.objects.none()

        qs = Cliente.objects.all()

        if self.q:
            qs = qs.filter(Q(ruc_cliente__istartswith=self.q) | Q(nombre_razon__istartswith=self.q))

        return qs

    def _get_fields_as_json(self, result):
        # return json.loads(serializers.serialize('json', [result]))[0]['fields']
        result = result.__dict__
        del result['_state']
        return result

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': result.pk,
                'text': self.get_result_label(result),
                'pk': result.pk,
                'fields': self._get_fields_as_json(result)
            } for result in context['object_list']
        ]

# ---------------------VISTA FACTURA --------------------------------

from tienda.models import Factura


def list_facturas(request):
    facturas = Factura.objects.all()
    inlineformset_factory
    return render(request, 'facturas.html', {'facturas': facturas})


def create_factura(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioFactura(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Factura creado correctamente.')
            return redirect('list_facturas')

        messages.error(request, 'Error al Factura.')
    else:
        form = FomularioFactura()

    return render(request, 'facturas-form.html', {'form': form})


def update_factura(request, id):
    try:
        factura = Factura.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioFactura(request.POST, request.FILES, instance=factura)

        if form.is_valid():
            form.save()
            messages.success(request, 'Factura actualizado correctamente.')
            return redirect('list_facturas')
        messages.error(request, 'Error al modificar Factura.')
    else:
        form = FomularioFactura(instance=factura)

    return render(request, 'facturas-form.html', {'form': form, 'factura': factura})


def delete_factura(request, id):
    try:
        factura = Factura.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        factura.delete()
        messages.success(request, 'Factura eliminado correctamente.')

    return redirect('list_facturas')




# ---------------------VISTA PRODUCTO --------------------------------
def list_productos(request):
    productos = Producto.objects.exclude(codigo='CUENTA')
    return render(request, 'producto.html', {'productos': productos})


def create_producto(request):

    if request.method == 'POST':

        form = FomularioProducto(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('list_productos')

        messages.error(request, 'Error al crear producto.')
    else:
        form = FomularioProducto()


    return render(request, 'producto-form.html', {'form': form})


def update_producto(request, codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioProducto(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto se ha actualizado correctamente.')
            return redirect('list_productos')
        messages.error(request, 'Error al modificar Producto.')
        print(form.errors)
    else:
        form = FomularioProducto(instance=producto)

    return render(request, 'producto-form.html', {'form': form, 'producto': producto})


def delete_producto(request, codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
    except:
        return redirect('404')

    if producto.codigo == 'CUOTA':
        messages.error(request, 'Cuota no puede ser borrado.')

    elif  request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')

    return redirect('list_productos')




# ---------------------VISTA VENTA CABECERA --------------------------------

def cuentas(formset):
    productos_cuenta = [] # indices de Productos que son cuenta
    for idx, form in enumerate(formset.cleaned_data):
        if 'producto' in form and form['producto'].codigo == 'CUENTA':
            productos_cuenta.append((idx, form['cantidad']))

    return productos_cuenta


def list_ventas(request):
    fecha = request.GET.get('fecha', None)
    if not fecha:
        fecha = datetime.date.today()
    else:
        fecha = datetime.datetime.strptime(fecha, settings.DATE_INPUT_FORMATS[0]).date()

    ventas = VentaCabecera.objects.filter(fecha=fecha,estado='A')
    pagos = Pago.objects.filter(venta__estado='A', venta__fecha=fecha)

    monto_efectivo = pagos.aggregate(total=Coalesce(Sum('monto_efectivo'), 0))
    monto_tarjeta = pagos.aggregate(total=Coalesce(Sum('monto_tarjeta'), 0))
    monto_cheque= pagos.aggregate(total=Coalesce(Sum('monto_cheque'), 0))
    suma_ventas = ventas.aggregate(total=Coalesce(Sum('monto_total'), 0))


    return render(request, 'ventas.html', { 'fecha': fecha,'ventas': ventas,
                                            'total': suma_ventas,
                                            'totale': monto_efectivo,
                                            'totalt': monto_tarjeta,
                                            'totalch': monto_cheque})

def list_ventas_canceladas(request):
    fecha = request.GET.get('fecha', None)
    if not fecha:
        fecha = datetime.date.today()
    else:
        fecha = datetime.datetime.strptime(fecha, settings.DATE_INPUT_FORMATS[0]).date()

    ventas = VentaCabecera.objects.filter(fecha=fecha,estado='IN')


    suma_ventas = ventas.aggregate(total=Sum('monto_total'))

    monto_suma = suma_ventas['total']
    if not monto_suma:
        monto_suma = 0

    return render(request, 'ventas-canceladas.html', { 'fecha': fecha,'ventas': ventas,
                                            'total': monto_suma})





# se listan las ventas y se tiene accion cancelar, colocar solo disponible para admin
def cancela_venta(request, id):
    try:
        venta = VentaCabecera.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        venta.estado = 'IN'
        venta.save()
        messages.success(request, 'VENTA CANCELADA CORRECTAMENTE.')
    return redirect('list_ventas')






def numero_factura(factura):
    """
    Funcion para obtener numero de la factura
    :param factura: objeto de tipo Factura
    :return: Siguiente numero de factura
    """
    # Completa con 0s

    maximo = VentaCabecera.objects.aggregate(maximo=Max('nro_factura_numero', filter=Q(talonario_factura_id=factura.id)))

    siguiente = maximo['maximo'] + 1 if maximo['maximo'] else factura.nro_inicial

    # el siguiente esta fuera del rango permitido, retorna None
    if factura.nro_inicial > siguiente or factura.nro_final < siguiente:
        return None


    return "{:07d}".format(siguiente)


def limpiar_pago(pago):
    pass
    # if pago.metodo_pago == 'Efectivo':
    #     pago.tarjeta = None
    #     pago.nro_autorizacion = None
    #     pago.ultimos_tarjeta = None
    #     pago.banco = None
    #     pago.nro_cuenta = None
    #     pago.librador = None
    #     pago.serie_cheque = None
    #     pago.nro_cheque = None
    #     pago.fecha_emision = None
    #     pago.fecha_venc = None
    # elif pago.metodo_pago == 'Tarjeta':
    #     pago.banco = None
    #     pago.nro_cuenta = None
    #     pago.librador = None
    #     pago.serie_cheque = None
    #     pago.nro_cheque = None
    #     pago.fecha_emision = None
    #     pago.fecha_venc = None
    # else:
    #     pago.tarjeta = None
    #     pago.nro_autorizacion = None
    #     pago.ultimos_tarjeta = None

def validar_pago(request):
    is_valid = True
    errors = {}
    pago = Pago()
    metodo_tarjeta = "pago-pago_tarjeta" in request.POST
    metodo_cheque = "pago-pago_cheque" in request.POST

    if metodo_tarjeta:
        formTarjeta = FormularioPagoTarjeta(request.POST, request.FILES, instance=pago, prefix='pago')
        is_valid = is_valid and formTarjeta.is_valid()
        for error in formTarjeta.errors:
            if error not in errors:
                errors[error] = []
            errors[error].append(formTarjeta.errors[error])

    if metodo_cheque:
        formCheque = FormularioPagoCheque(request.POST, request.FILES, instance=pago, prefix='pago')
        is_valid = is_valid and formCheque.is_valid()
        for error in formCheque.errors:
            if error not in errors:
                errors[error] = []
            errors[error].append(formCheque.errors[error])

    return is_valid, errors

def vender(request):

    venta = VentaCabecera()
    pago= Pago()
    cuenta = Producto.objects.get(codigo='CUENTA')
    FormularioDetalleSet = inlineformset_factory(VentaCabecera, VentaDetalle, extra=0, can_delete=True,
                                                 form=FormularioVentaDetalle, min_num=1)

    if request.method == 'POST':

        form = FormularioVentaVerificar(request.POST, request.FILES,instance=venta)
        formularioDetalleSet = FormularioDetalleSet(request.POST, request.FILES, instance=venta)
        formularioPago = FormularioPago(request.POST, request.FILES, instance=pago,prefix='pago')

        ruc_cliente = request.POST['cliente-ruc_cliente']

        try:
            cliente = Cliente.objects.get(ruc_cliente=ruc_cliente)
        except:
            cliente = Cliente()

        formularioCliente = FormularioCliente(request.POST, request.FILES, prefix='cliente', instance=cliente)
        pagos_validacion = validar_pago(request)
        try:
            # Ejecuta todos los is_valid, para calcular los errores
            form.is_valid()
            formularioDetalleSet.is_valid()
            formularioCliente.is_valid()
            formularioPago.is_valid()

            if form.is_valid() and len(formularioDetalleSet) > 0 \
                    and formularioDetalleSet.is_valid() and formularioCliente.is_valid() \
                    and formularioPago.is_valid() and pagos_validacion[0]:
                cliente = formularioCliente.save()
                venta = form.save(commit=False)
                venta.cliente = cliente
                venta.save()
                detalles = formularioDetalleSet.save()
                pago=formularioPago.save(commit=False)
                pago.venta = venta
                limpiar_pago(pago)
                pago.save()


                for detalle in detalles:
                    detalle.descripcion = detalle.producto.nombre

                    if detalle.producto.control_stock:
                        detalle.producto.existencia -= detalle.cantidad
                        detalle.producto.save()

                    detalle.save()


                productos_cuenta = cuentas(formularioDetalleSet)


                if productos_cuenta:
                    for idx, cantidad in productos_cuenta:
                        cuenta_a_pagar = Cuenta.objects.get(pk=request.POST['ventadetalle_set-' + str(idx) + '-cuenta'])
                        cuenta_a_pagar.pagado = True
                        cuenta_a_pagar.monto_pagado = detalles[idx].precio
                        cuenta_a_pagar.detalle = detalles[idx]
                        cuenta_a_pagar.save()
                        anterior = cuenta_a_pagar
                        # cuando se paga mas de una cuota
                        for i in range(1, cantidad):
                            cuenta_adelantada = Cuenta.objects.get_or_create(inscripcion=anterior.inscripcion,
                                                                             vencimiento=calcular_fecha(anterior.vencimiento.day, anterior.vencimiento))[0]
                            cuenta_adelantada.monto = anterior.monto
                            cuenta_adelantada.monto_pagado = anterior.monto_pagado
                            cuenta_adelantada.pagado = True
                            cuenta_adelantada.detalle = detalles[idx]
                            cuenta_adelantada.save()
                            anterior = cuenta_adelantada

                messages.success(request, 'Venta registrada correctamente')
                return JsonResponse({'success':True, 'redirect': reverse('consulta_factura', kwargs={'nro_factura': venta.nro_factura})}, safe=False)
        except IntegrityError as e:
            logger.exception("No se pudo guardar la venta")

        transaction.set_rollback(True)
        return JsonResponse({'success':False, 'formErrors': form.errors,
                             'detalleErrors': formularioDetalleSet.errors, 'clienteErrors': formularioCliente.errors,
                             'pagoErrors': formularioPago.errors, 'pagoErrorsExtra': pagos_validacion[1]} , safe=False)
    else:
        hoy = datetime.datetime.today()
        # Trae solo lo vigente y activo
        talonario = Factura.objects.filter(Q(vigencia_desde__lte=hoy) & Q(vigencia_hasta__gte=hoy) & Q(estado='A')).first()
        if not talonario:
            messages.error(request, 'No se puede realizar la venta, no hay talonarios de factura vigentes')
            return redirect('list_facturas')

        nro_factura = numero_factura(talonario)
        if not nro_factura:
            messages.error(request, 'No se puede realizar la venta, debe dar de baja el talonario '+ str(talonario))
            return redirect('list_facturas')

        cliente = Cliente()
        form = FormularioVenta(instance=venta)
        formularioDetalleSet = FormularioDetalleSet(instance=venta)
        formularioCliente = FormularioCliente(instance=cliente, prefix='cliente')
        formularioPago= FormularioPago(instance=pago, prefix='pago')

    return render(request, 'ventas-form.html', {'form': form, 'formularioDetalleSet': formularioDetalleSet,
                                                'talonario': talonario, 'nro_factura': nro_factura,
                                                'formularioCliente': formularioCliente,
                                                'cuenta': cuenta, 'formularioPago':formularioPago})

# ---------------------VISTA COMPRA CABECERA --------------------------------

def list_compras(request):

    fecha = request.GET.get('fecha', None)
    if not fecha:
        fecha = datetime.date.today()
    else:
        fecha = datetime.datetime.strptime(fecha, settings.DATE_INPUT_FORMATS[0]).date()

    compras = CompraCabecera.objects.filter(fecha=fecha)



    suma_compras = compras.aggregate(total=Sum('monto_total'))

    monto_suma = suma_compras['total']
    if not monto_suma:
        monto_suma = 0

    return render(request, 'compras.html', { 'fecha': fecha,'compras': compras,
                                            'total': monto_suma})








class RequiredFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

def comprar(request):
    compra = CompraCabecera()

    FormularioDetalleSet = inlineformset_factory(CompraCabecera, CompraDetalle, extra=0,
                                                 can_delete=True, min_num=1, validate_min=True,
                                                 form=FormularioCompraDetalle, formset=RequiredFormSet)

    if request.method == 'POST':

        form = FormularioCompra(request.POST, request.FILES,instance=compra)
        formularioDetalleSet = FormularioDetalleSet(request.POST, request.FILES,instance=compra)

        if form.is_valid() and formularioDetalleSet.is_valid():
            form.save()
            formularioDetalleSet.save()
            messages.success(request, 'Compra registrada correctamente')
            return redirect('list_compras')

        messages.error(request, 'Error al registrar egreso. Verifique los campos')
    else:
        form = FormularioCompra(instance=compra)
        formularioDetalleSet=FormularioDetalleSet(instance=compra)



    return render(request, 'compras-form.html', {'form': form, 'formularioDetalleSet': formularioDetalleSet})

def update_compra(request, id):
    try:
        compra = CompraCabecera.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioFactura(request.POST, request.FILES, instance=compra)

        if form.is_valid():
            form.save()
            messages.success(request, 'Compra actualizado correctamente.')
            return redirect('list_compras')
        messages.error(request, 'Error al modificar Compra.')
    else:
        form = FomularioFactura(instance=compra)

    return render(request, 'compras-form.html', {'form': form, 'compras': compra})




# ---------------------VISTA COMPRA DETALLE --------------------------------

def list_detalle_compra(request):
    detalle = CompraCabecera.objects.all()
    return render(request, 'compras-detalle.html', {'detalles': detalle})




def agrega_detalle(request):
    if request.method == 'POST':

        form = FormularioCompraDetalle(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'detalle registrada correctamente')
            return redirect('list_detalle_compras')

        messages.error(request, 'Error al crear detalle.')
    else:
        form = FormularioCompraDetalle()


    return render(request, 'compras-form.html', {'form': form})

def update_compra_detalle(request, id):
    try:
        detalle = CompraDetalle.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FormularioCompraDetalle(request.POST, request.FILES, instance=detalle)

        if form.is_valid():
            form.save()
            messages.success(request, 'detalle actualizado correctamente.')
            return redirect('list_detalle_compra')
        messages.error(request, 'Error al modificar detalle.')
    else:
        form = FormularioCompraDetalle(instance=detalle)

    return render(request, 'compras-detalle-form.html', {'form': form, 'detalles': detalle})





def update_factura(request, id):
    try:
        factura = Factura.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioFactura(request.POST, request.FILES, instance=factura)

        if form.is_valid():
            form.save()
            messages.success(request, 'Factura actualizado correctamente.')
            return redirect('list_facturas')
        messages.error(request, 'Error al modificar Factura.')
    else:
        form = FomularioFactura(instance=factura)

    return render(request, 'facturas-form.html', {'form': form, 'factura': factura})

# probando reporte

import csv

from django.http import HttpResponse, JsonResponse
from .models import Producto


def export_productos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['codigo', 'nombre', 'foto_producto', 'descripcion', 'control_stock','precio_venta','costo','iva','estado'])
    productos = Producto.objects.all().values_list('codigo', 'nombre','foto_producto','descripcion','precio_venta','costo','iva','estado')
    for producto in productos:
        writer.writerow(producto)

    return response

def reporte_compras(request):
    form = FormularioReporteCompras()
    if request.method == 'POST':
        form = FormularioReporteCompras(request.POST)
        if form.is_valid():
            # Obtener los objetos que deseas exportar e iterar
            # filtrado por los campos del formulario
            # ['fecha', 'nro_factura', 'ruc_proveedor', 'proveedor', 'monto_total']
            objetos = CompraCabecera.objects.filter(
                fecha=form.cleaned_data.get('fecha'),
                nro_factura=form.cleaned_data.get('nro_factura'),
                ruc_proveedor=form.cleaned_data.get('ruc_proveedor'),
                monto_total=form.cleaned_data.get('monto_total')
            )

            # Crear el objeto HttpResponse con sus cabeceras
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="reporte.csv"'

            # Se usa el response como un "archivo" destino
            writer = csv.writer(response)

            for objeto in objetos:
                row = [
                    objeto.fecha,
                    objeto.nro_factura,
                    objeto.ruc_proveedor,
                    objeto.monto_total

                ]
                writer.writerow(row)
            return response
    return render(request, 'compras_reporte-form.html', {'form': form})





# ---------------------VISTA CLIENTES--------------------------------

from tienda.models import Cliente


def list_clientes(request):
    clientes = Cliente.objects.all()

    return render(request, 'clientes.html', {'clientes': clientes})


def create_cliente(request):
    print(request.method)
    if request.method == 'POST':

        form = FormularioCliente(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('list_clientes')

        messages.error(request, 'Error al crear cliente.')
    else:
        form = FormularioCliente()

    return render(request, 'clientes-form.html', {'form': form})



def update_cliente(request, ruc_cliente):
    try:
        cliente = Cliente.objects.get(ruc_cliente=ruc_cliente)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FormularioCliente(request.POST, request.FILES, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('list_clientes')
        messages.error(request, 'Error al modificar Cliente.')
    else:
        form = FormularioCliente(instance=cliente)

    return render(request, 'clientes-form.html', {'form': form, 'cliente': cliente})


def delete_cliente(request, ruc_cliente):
    try:
        cliente = Cliente.objects.get(ruc_cliente=ruc_cliente)
    except:
        return redirect('404')

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')

    return redirect('list_clientes')


def consulta_factura(request, nro_factura):
    cabecera = VentaCabecera.objects.get(nro_factura=nro_factura)
    pago = Pago.objects.get(venta=cabecera)
    detalles = VentaDetalle.objects.filter(venta__nro_factura=nro_factura)
    talonario = cabecera.talonario_factura
    context = {'detalles': detalles, 'talonario': talonario, 'cabecera': cabecera, 'pago': pago}
    return render(request, 'venta-detalle.html', context)



# OPERACIONES EN CAJA

def list_operaciones(request):
    fecha = request.GET.get('fecha', None)
    if not fecha:
        fecha = datetime.date.today()
    else:
        fecha = datetime.datetime.strptime(fecha, settings.DATE_INPUT_FORMATS[0]).date()

    operacion = OperacionCaja.objects.filter(fecha=fecha)
    entradas = operacion.filter(tipo_transaccion='ENTRADA').aggregate(total=Sum('monto'))
    salidas = operacion.filter(tipo_transaccion='SALIDA').aggregate(total=Sum('monto'))

    monto_salida = salidas['total']
    monto_entrada = entradas['total']

    if not monto_salida:
        monto_salida = 0
    if not monto_entrada:
        monto_entrada = 0

    return render(request, 'operacion_caja.html', {'operaciones': operacion, 'fecha': fecha,
                                                   'total': monto_entrada -  monto_salida })



def create_operacion(request):
    print(request.method)
    if request.method == 'POST':

        form = FormularioOperacionCaja(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'operacion creada correctamente.')
            return redirect('list_operaciones')

        messages.error(request, 'Error al crear operacion.')
    else:
        form = FormularioOperacionCaja()

    return render(request, 'operacion_caja-form.html', {'form': form})


def update_operacion(request, id):
    try:
        operacion = OperacionCaja.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FormularioOperacionCaja(request.POST, request.FILES, instance=operacion)

        if form.is_valid():
            form.save()
            messages.success(request, 'operacion actualizado correctamente.')
            return redirect('list_operaciones')
        messages.error(request, 'Error al modificar operacion.')
    else:
        form = FormularioOperacionCaja(instance=operacion)

    return render(request, 'operacion_caja-form.html', {'form': form, 'operacion': operacion})


def delete_operacion(request, id):
    try:
        operacion = OperacionCaja.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        operacion.delete()
        messages.success(request, 'operacion eliminado correctamente.')

    return redirect('list_operaciones')


def estado_cuenta(request):

    cedula = request.GET.get('cedula', None)

    if request.method == 'POST':
        inscripcion = request.POST['inscripcion']

        # ultima cuenta de inscripción
        ultima_cuenta = Cuenta.objects.filter(inscripcion_id=inscripcion).order_by('-vencimiento').first()

        cuenta = Cuenta()
        cuenta.inscripcion_id = inscripcion
        cuenta.monto = ultima_cuenta.monto

        cuenta.vencimiento = calcular_fecha(ultima_cuenta.vencimiento.day, ultima_cuenta.vencimiento)
        print(ultima_cuenta.vencimiento)
        print(cuenta.vencimiento)
        cuenta.save()

    resultados = []

    persona = None

    if cedula:

        persona = Persona.objects.get(cedula=cedula)
        query = """
        select
      pa.nombre alumno_nombre,
      pa.apellido alumno_apellido,
      pa.cedula alumno_cedula,
      pt.nombre,
      pt.apellido,
      pt.cedula,
      g.hora_fin,
      g.hora_inicio,
      g.lunes,
      g.martes,
      g.miercoles,
      g.jueves,
      g.viernes,
      g.sabado,
      g.domingo,
      cl.nombre nombre_curso,
      i.id inscripcion,
      i.fecha_inicio,
      i.fecha_fin,
      i.estado,
      cuenta.vencimiento,
      cuenta.pagado
from escuela_inscripcion i
  join escuela_grupo g on i.grupo_id = g.id
  join escuela_clase cl on g.id_clase_id = cl.id
  join main_alumno a on i.alumno_id = a.persona_ptr_id
  join main_titular t on a.titular_cuenta_id = t.persona_ptr_id
  join main_persona pt on t.persona_ptr_id = pt.id
  join main_persona pa on a.persona_ptr_id = pa.id
  join escuela_cuenta cuenta on i.id = cuenta.inscripcion_id
where (pt.cedula = %(cedula)s or pa.cedula = %(cedula)s) and i.estado = 'A'
and cuenta.vencimiento = (select c.vencimiento
                             from escuela_cuenta c
                             where c.inscripcion_id = i.id
                             order by c.vencimiento desc
                             limit 1);
        """
        cursor = connection.cursor()
        cursor.execute(query, {'cedula': cedula})
        resultados = dictfetch(cursor, 1000, 0)

        def agrega_grupo(resultado):
            resultado['grupo'] = Grupo(
                hora_fin=resultado['hora_fin'],
                hora_inicio=resultado['hora_inicio'],
                lunes=resultado['lunes'],
                martes=resultado['martes'],
                miercoles=resultado['miercoles'],
                jueves=resultado['jueves'],
                viernes=resultado['viernes'],
                sabado=resultado['sabado'],
                domingo=resultado['domingo'],
            )
            return resultado

        resultados = map(agrega_grupo, resultados)

    context = {'resultados': resultados, 'persona': persona, 'cedula': cedula}

    return render(request, 'estado_cuenta.html', context=context)