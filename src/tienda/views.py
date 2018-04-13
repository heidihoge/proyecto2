from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import FomularioCategoriaProducto, FomularioProducto
from .models import Producto, CategoriaProducto

# Create your views here.

# ---------------------VISTA TIPODOCUMENTO --------------------------------
# from compra_venta.forms import FomularioDocumento
# from compra_venta.models import TipoDocumento
#
#
# def list_documentos(request):
#     documentos = TipoDocumento.objects.all()
#     return render(request, 'documentos.html', {'documentos': documentos})
#
#
# def create_documento(request):
#     print(request.method)
#     if request.method == 'POST':
#
#         form = FomularioDocumento(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Documento creado correctamente.')
#             return redirect('list_documentos')
#
#         messages.error(request, 'Error al crear asistencia.')
#     else:
#         form = FomularioDocumento()
#
#     return render(request, 'documentos-form.html', {'form': form})
#
#
# def update_documento(request, id):
#     try:
#         documento = TipoDocumento.objects.get(id=id)
#     except:
#         return redirect('404')
#     if request.method == 'POST':
#         form = FomularioDocumento(request.POST, request.FILES, instance=documento)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Documento actualizado correctamente.')
#             return redirect('list_documentos')
#         messages.error(request, 'Error al modificar Documento.')
#     else:
#         form = FomularioDocumento(instance=documento)
#
#     return render(request, 'documentos-form.html', {'form': form, 'documentos': documento})
#
#
# def delete_documento(request, id):
#     try:
#         documento = TipoDocumento.objects.get(id=id)
#     except:
#         return redirect('404')
#
#     if request.method == 'POST':
#         documento.delete()
#         messages.success(request, 'Documento eliminado correctamente.')
#
#     return redirect('list_documentos')

# ---------------------VISTA TIMBRADO --------------------------------

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
