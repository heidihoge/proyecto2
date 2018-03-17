from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ClaseForm
from .models import Clase


def list_clases(request):
    clases = Clase.objects.all()
    return render(request, 'clases/clases.html', {'clases': clases})


def create_clase(request):
    print(request.method)
    if request.method == 'POST':

        form = ClaseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Clase fue creado correctamente.')
            return redirect('list_clases')

        messages.error(request, 'Error al crear Clase.')
    else:
        form = ClaseForm()

    return render(request, 'clases/clases-form.html', {'form': form})


def update_clase(request, id):
    try:
        clase = Clase.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = ClaseForm(request.POST, request.FILES, instance=clase)

        if form.is_valid():
            form.save()
            messages.success(request, 'Clase fue actualizado correctamente.')
            return redirect('list_clases')
        messages.error(request, 'Error al modificar la Clase.')
    else:
        form = ClaseForm(instance=clase)

    return render(request, 'clases/clases-form.html', {'form': form, 'clase': clase})


def delete_clase(request, id):
    clase = Clase.objects.get(id=id)

    if request.method == 'POST':
        clase.delete()
        messages.success(request, 'Clase eliminada correctamente.')

    return redirect('list_clases')
