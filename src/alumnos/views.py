from django.shortcuts import render, redirect
from .models import Alumno
from .forms import AlumnoForm


def list_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/alumnos.html', {'alumnos': alumnos})


def create_alumno(request):
    form = AlumnoForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return redirect('list_alumnos')

    return render(request, 'alumnos/alumnos-form.html', {'form': form})


def update_alumno(request, id):
    alumno = Alumno.objects.get(id=id)
    form = AlumnoForm(request.POST , instance=alumno)

    if form.is_valid():
        form.save()
        return redirect('list_alumnos')

    return render(request, 'alumnos/alumnos-form.html', {'form': form, 'alumno': alumno})


def delete_alumno(request, id):
    alumno = Alumno.objects.get(id=id)

    if request.method == 'POST':
        alumno.delete()
        return redirect('list_alumnos')

    return render(request, 'alumnos/alum-delete-confirm.html', {'alumno': alumno})