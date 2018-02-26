from django.shortcuts import render, redirect
from .models import Profesor
from .forms import ProfesorForm
from django.contrib import messages


def list_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesores/profesores.html', {'profesores': profesores})


def create_profesor(request):
    print(request.method)
    if request.method == 'POST':

        form = ProfesorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profesor creado correctamente.')
            return redirect('list_profesores')

        messages.error(request, 'Error al crear el Profesor.')
    else:
        form = ProfesorForm()

    return render(request, 'profesores/profesores-form.html', {'form': form})


def update_profesor(request, id):
    try:
        profesor = Profesor.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = ProfesorForm(request.POST, request.FILES, instance=profesor)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profesor actualizado correctamente.')
            return redirect('list_profesores')
        messages.error(request, 'Error al modificar el Profesor.')
    else:
        form = ProfesorForm(instance=profesor)

    return render(request, 'profesores/profesores-form.html', {'form': form, 'profesor': profesor})


def delete_profesor(request, id):
    profesor = Profesor.objects.get(id=id)

    if request.method == 'POST':
        profesor.delete()
        messages.success(request, 'Profesor eliminado correctamente.')

    return redirect('list_profesores')