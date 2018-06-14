import datetime
from dal import autocomplete
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.db.models import Q, Max
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from escuela.models import Cuenta
from proyecto2 import settings
from .forms import FomularioFactura, FormularioCompra, FormularioCompraDetalle, FormularioVentaDetalle, FormularioVenta, \
    FormularioCliente, FomularioCliente, FormularioVentaVerificar, FormularioOperacionCaja, FormularioPago, \
    FormularioReporteCompras

from .forms import  FomularioProducto
from .models import Producto, CompraCabecera, CompraDetalle, VentaCabecera, VentaDetalle, Cliente, OperacionCaja, Pago


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

        return qs


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


        if self.q:
            qs = qs.filter(Q(inscripcion__alumno__cedula__istartswith=self.q) |
                           Q(inscripcion__alumno__titular_cuenta__cedula__istartswith=self.q))

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
        if form['producto'].codigo == 'CUENTA':
            productos_cuenta.append(idx)

    return productos_cuenta


def list_ventas(request):
    venta = VentaCabecera.objects.all()
    return render(request, 'ventas.html', {'ventas': venta})


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


def verificar_pago(pago):
    if pago.metodo_pago == 'Efectivo':
        pago.tarjeta = None
        pago.nro_autorizacion = None
        pago.ultimos_tarjeta = None
        pago.banco = None
        pago.nro_cuenta = None
        pago.librador = None
        pago.serie_cheque = None
        pago.nro_cheque = None
        pago.fecha_emision = None
        pago.fecha_venc = None
    elif pago.metodo_pago == 'Tarjeta':
        pago.banco = None
        pago.nro_cuenta = None
        pago.librador = None
        pago.serie_cheque = None
        pago.nro_cheque = None
        pago.fecha_emision = None
        pago.fecha_venc = None
    else:
        pago.tarjeta = None
        pago.nro_autorizacion = None
        pago.ultimos_tarjeta = None


    pass


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


def vender(request):

    venta = VentaCabecera()
    pago= Pago()
    cuenta = Producto.objects.get(codigo='CUENTA')
    FormularioDetalleSet = inlineformset_factory(VentaCabecera, VentaDetalle, extra=0, can_delete=True, form=FormularioVentaDetalle)

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

        if form.is_valid() and formularioDetalleSet.is_valid() and formularioCliente.is_valid() and formularioPago.is_valid():
            cliente = formularioCliente.save()
            venta = form.save(commit=False)
            venta.cliente = cliente
            venta.save()
            detalles = formularioDetalleSet.save()
            pago=formularioPago.save(commit=False)
            pago.venta = venta
            verificar_pago(pago)
            pago.save()


            for detalle in detalles:
                detalle.descripcion = detalle.producto.nombre

                if detalle.producto.control_stock:
                    detalle.producto.existencia -= detalle.cantidad
                    detalle.producto.save()

                detalle.save()


            productos_cuenta = cuentas(formularioDetalleSet)


            if productos_cuenta:
                for idx in productos_cuenta:
                    cuenta_a_pagar = Cuenta.objects.get(pk=request.POST['ventadetalle_set-' + str(idx) + '-cuenta'])
                    cuenta_a_pagar.pagado = True
                    cuenta_a_pagar.monto_pagado = detalles[idx].precio
                    cuenta_a_pagar.detalle = detalles[idx]
                    cuenta_a_pagar.save()

            messages.success(request, 'Venta registrada correctamente')
            return JsonResponse({'success':True}, safe=False)

        return JsonResponse({'success':False, 'formErrors': form.errors,
                             'detalleErrors': formularioDetalleSet.errors, 'clienteErrors': formularioCliente.errors,
                             'pagoErrors': formularioPago.errors} , safe=False)
    else:
        hoy = datetime.datetime.today()
        # Trae solo lo vigente y activo
        talonario = Factura.objects.filter(Q(vigencia_desde__lte=hoy) & Q(vigencia_hasta__gte=hoy) & Q(estado='A')).first()

        cliente = Cliente()
        form = FormularioVenta(instance=venta)
        formularioDetalleSet = FormularioDetalleSet(instance=venta)
        formularioCliente = FormularioCliente(instance=cliente, prefix='cliente')
        formularioPago= FormularioPago(instance=pago, prefix='pago')

    return render(request, 'ventas-form.html', {'form': form, 'formularioDetalleSet': formularioDetalleSet,
                                                'talonario': talonario, 'nro_factura': numero_factura(talonario),
                                                'formularioCliente': formularioCliente,
                                                'cuenta': cuenta, 'formularioPago':formularioPago})

# ---------------------VISTA COMPRA CABECERA --------------------------------

def list_compras(request):
    compras = CompraCabecera.objects.all()
    return render(request, 'compras.html', {'compras': compras})




def comprar(request):
    compra = CompraCabecera()

    FormularioDetalleSet = inlineformset_factory(CompraCabecera, CompraDetalle, extra=0, can_delete=True, form=FormularioCompraDetalle)

    if request.method == 'POST':

        form = FormularioCompra(request.POST, request.FILES,instance=compra)
        formularioDetalleSet = FormularioDetalleSet(request.POST, request.FILES,instance=compra)

        if form.is_valid() and formularioDetalleSet.is_valid():
            form.save()
            formularioDetalleSet.save()
            messages.success(request, 'Compra registrada correctamente')
            return redirect('list_compras')

        messages.error(request, 'Error al crear producto.')
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

        form = FomularioCliente(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('list_clientes')

        messages.error(request, 'Error al crear cliente.')
    else:
        form = FomularioCliente()

    return render(request, 'clientes-form.html', {'form': form})



def update_cliente(request, ruc_cliente):
    try:
        cliente = Cliente.objects.get(ruc_cliente=ruc_cliente)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioCliente(request.POST, request.FILES, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('list_clientes')
        messages.error(request, 'Error al modificar Cliente.')
    else:
        form = FomularioCliente(instance=cliente)

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
    detalles = VentaDetalle.objects.filter(venta__nro_factura=nro_factura)
    context = {'detalles': detalles}
    return render(request, 'venta-detalle.html', context)



# OPERACIONES EN CAJA

def list_operaciones(request):
    operacion = OperacionCaja.objects.all()

    return render(request, 'operacion_caja.html', {'operaciones': operacion})




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