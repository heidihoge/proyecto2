from django.shortcuts import render

# Create your views here.

# ---------------------VISTA TIPODOCUMENTO --------------------------------
from compra_venta.models import TipoDocumento


def list_documentos(request):
    documento = TipoDocumento.objects.all()
    return render(request, 'documentos.html', {'documento': documento})


def create_tipo_documento(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioDocumento(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Documento creado correctamente.')
            return redirect('list_documentos')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_documentos')

# ---------------------VISTA TIMBRADO --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA CATEGORIA PRODUCTO --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA PRODUCTO --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA EXISTENCIA --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA TIPO PAGO --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA COMPRA CABECERA --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA COMPRA DETALLE --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA VENTA CABECERA --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA VENTA DETALLE --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')

# ---------------------VISTA PAGOS --------------------------------
def list_asistencias(request):
    asistencia = Asistencia.objects.all()
    return render(request, 'asistencias.html', {'asistencias': asistencia})


def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('list_asistencias')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FomularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioAsistencia(request.POST, request.FILES, instance=asistencia)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia actualizada correctamente.')
            return redirect('list_asistencias')
        messages.error(request, 'Error al modificar Asistencia.')
    else:
        form = FomularioAsistencia(instance=asistencia)

    return render(request, 'clases-form.html', {'form': form, 'asistencias': asistencia})


def delete_asistencia(request, id):
    try:
        asistencia = Asistencia.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente.')

    return redirect('list_asistencias')
