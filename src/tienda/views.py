from django.contrib import messages
from django.shortcuts import render, redirect

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

# ---------------------VISTA PRODUCTO --------------------------------

# ---------------------VISTA EXISTENCIA --------------------------------

# ---------------------VISTA TIPO PAGO --------------------------------

# ---------------------VISTA COMPRA CABECERA --------------------------------

# ---------------------VISTA COMPRA DETALLE --------------------------------

# ---------------------VISTA VENTA CABECERA --------------------------------

# ---------------------VISTA VENTA DETALLE --------------------------------

# ---------------------VISTA PAGOS --------------------------------
