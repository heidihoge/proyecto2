from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import FomularioFactura

from .forms import FomularioCategoriaProducto, FomularioProducto
from .models import Producto, CategoriaProducto

# Create your views here.

# ---------------------VISTA FACTURA --------------------------------

from tienda.models import Factura


def list_facturas(request):
    facturas = Factura.objects.all()
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



# ---------------------VISTA CATEGORIA PRODUCTO --------------------------------
def list_categoria_productos(request):
    categoria_producto = CategoriaProducto.objects.all()
    return render(request, 'categoria_producto.html', {'categoria_producto': categoria_producto})


def create_categoria_producto(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioCategoriaProducto(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria creada correctamente.')
            return redirect('list_categoria_productos')

        messages.error(request, 'Error al crear categoria.')
    else:
        form = FomularioCategoriaProducto()

    return render(request, 'categoria_producto-form.html', {'form': form})


def update_categoria_producto(request, id):
    try:
        categoria_producto = CategoriaProducto.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioProducto(request.POST, request.FILES, instance=categoria_producto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria actualizada correctamente.')
            return redirect('list_categoria_productos')
        messages.error(request, 'Error al modificar Categoria.')
    else:
        form = FomularioCategoriaProducto(instance=categoria_producto)

    return render(request, 'categoria_producto.html', {'form': form, 'categoria_producto': categoria_producto})


def delete_categoria_producto(request, id):
    try:
         categoria_producto = CategoriaProducto.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        categoria_producto.delete()
        messages.success(request, 'Categoria eliminada correctamente.')

    return redirect('list_categoria_productos')

# ---------------------VISTA PRODUCTO --------------------------------
def list_productos(request):
    producto = Producto.objects.all()
    return render(request, 'producto.html', {'producto': producto})


def create_producto(request):
    print(request.method)
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


def update_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioProducto(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Producto se ha actualizado correctamente.')
            return redirect('list_productos')
        messages.error(request, 'Error al modificar Producto.')
    else:
        form = FomularioProducto(instance=producto)

    return render(request, 'producto.html', {'form': form, 'producto': producto})


def delete_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')

    return redirect('list_productos')

# ---------------------VISTA EXISTENCIA --------------------------------

# ---------------------VISTA TIPO PAGO --------------------------------

# ---------------------VISTA COMPRA CABECERA --------------------------------

# ---------------------VISTA COMPRA DETALLE --------------------------------

# ---------------------VISTA VENTA CABECERA --------------------------------

# ---------------------VISTA VENTA DETALLE --------------------------------

# ---------------------VISTA PAGOS --------------------------------
