from django.shortcuts import render, redirect
from .models import Alumno
from .forms import AlumnoForm
from django.contrib import messages

def list_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/alumnos.html', {'alumnos': alumnos})


def create_alumno(request):
    print(request.method)
    if request.method == 'POST':

        form = AlumnoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno creado correctamente.')
            return redirect('list_alumnos')

        messages.error(request, 'Error al crear el Alumno.')
    else:
        form = AlumnoForm()

    return render(request, 'alumnos/alumnos-form.html', {'form': form})


def update_alumno(request, id):
    try:
        alumno = Alumno.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES, instance=alumno)

        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno actualizado correctamente.')
            return redirect('list_alumnos')
        messages.error(request, 'Error al modificar el Alumno.')
    else:
        form = AlumnoForm(instance=alumno)

    return render(request, 'alumnos/alumnos-form.html', {'form': form, 'alumno': alumno})


def delete_alumno(request, id):
    alumno = Alumno.objects.get(id=id)

    if request.method == 'POST':
        alumno.delete()
        messages.success(request, 'Alumno eliminado correctamente.')
        
    return redirect('list_alumnos')