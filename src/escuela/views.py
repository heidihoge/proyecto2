from __future__ import unicode_literals

from dal import autocomplete
from django import forms
from django.shortcuts import render

from main.forms import TitularForm, AlumnoForm

menus = {
    "ajustes": {
        "url": "/admin",
        "img": "admin/img/ajustes.png",
        "title": "ADMINISTRACIÓN",
        "desc": "Ajustes de contenidos",
    },
    "natacion": {
        "url": "/admin",
        "img": "admin/img/natacion.png",
        "title": "GESTION DE CURSOS",
        "desc": "Cursos y horarios",
    },
    "indumentaria": {
        "url": "/admin",
        "img": "admin/img/indumentaria.png",
        "title": "VENTAS",
        "desc": "Uniformes",
    },
    "inscripcion": {
        "url": "/",
        "img": "admin/img/inscripcion.png",
        "title": "GESTION DE ALUMNOS",
        "desc": "Incripciones",
    },
    "asistencia": {
        "url": "/admin",
        "img": "admin/img/asistencia.png",
        "title": "ASISTENCIA",
        "desc": "Control de asitencia",
    },
    "cobranza": {
        "url": "/admin",
        "img": "admin/img/cobranza.png",
        "title": "COBRANZAS",
        "desc": "Cobro de cuotas",
    },
    "analitica": {
        "url": "/admin",
        "img": "admin/img/analitica.png",
        "title": "REPORTES",
        "desc": "Ingresos/Egresos",
    }
}

# Create your views here.
def inicio(request):

    context = {
        "menus": menus
    }

    return render(request,"inicio.html",context)


def principal (request):
    return render(request, "base.html")



from django.contrib import messages
from django.shortcuts import render, redirect


from .forms import FomularioClase,FomularioGrupo, FomularioAsistencia, FomularioDiaHora, FomularioEtiqueta, FomularioEtiquetaClase, FomularioEtiquetaGrupo, FomularioInscripcion
from .models import Clase,Grupo,Etiqueta, EtiquetaGrupo, EtiquetaClase, Inscripcion, Asistencia, DiaHora



# ---------------------VISTA CLASE --------------------------------

class ClaseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Clase.objects.none()

        qs = Clase.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)

        return qs

def list_clases(request):
    clase = Clase.objects.all()
    return render(request, 'clases.html', {'clases': clase})


def create_clase(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioClase(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Clase creada correctamente.')
            return redirect('list_clases')

        messages.error(request, 'Error al crear la clase.')
    else:
        form = FomularioClase()

    return render(request, 'clases-form.html', {'form': form})


def update_clase(request, id):
    try:
        clase = Clase.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioClase(request.POST, request.FILES, instance=clase)

        if form.is_valid():
            form.save()
            messages.success(request, 'Clase actualizada correctamente.')
            return redirect('list_clases')
        messages.error(request, 'Error al modificar Clase.')
    else:
        form = FomularioClase(instance=clase)

    return render(request, 'clases-form.html', {'form': form, 'clase': clase})


def delete_clase(request, id):
    try:
        clase = Clase.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        clase.delete()
        messages.success(request, 'Clase eliminada correctamente.')

    return redirect('list_clases')


# ---------------------VISTA GRUPO --------------------------------

def list_grupos(request):
    grupo = Grupo.objects.all()
    return render(request, 'grupos.html', {'grupos': grupo})


def create_grupo(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioGrupo(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo creada correctamente.')
            return redirect('list_grupos')

        messages.error(request, 'Error al crear el grupo.')
    else:
        form = FomularioGrupo()

    return render(request, 'grupos-form.html', {'form': form})


def update_grupo(request, id):
    try:
        grupo = Grupo.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioGrupo(request.POST, request.FILES, instance=grupo)

        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo actualizado correctamente.')
            return redirect('list_grupos')
        messages.error(request, 'Error al modificar Grupo.')
    else:
        form = FomularioGrupo(instance=grupo)

    return render(request, 'grupos-form.html', {'form': form, 'clase': grupo})


def delete_grupo(request, id):
    try:
        grupo = Grupo.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'Grupo eliminado correctamente.')

    return redirect('list_grupos')


# ---------------------VISTA DIA_HORA --------------------------------
def list_dia_horas(request):
    dia_hora = DiaHora.objects.all()
    return render(request, 'dia_horas.html', {'dia_horas': dia_hora})


def create_dia_hora(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioDiaHora(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Dia_hora creada correctamente.')
            return redirect('list_dia_horas')

        messages.error(request, 'Error al crear dias y horas.')
    else:
        form = FomularioDiaHora()

    return render(request, 'dia_horas-form.html', {'form': form})


def update_dia_hora(request, id):
    try:
        dia_hora = DiaHora.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioDiaHora(request.POST, request.FILES, instance=dia_hora)

        if form.is_valid():
            form.save()
            messages.success(request, 'DIA Y HORA actualizado correctamente.')
            return redirect('list_dia_horas')
        messages.error(request, 'Error al modificar DIA Y HORA.')
    else:
        form = FomularioDiaHora(instance=dia_hora)

    return render(request, 'dia_horas.html', {'form': form, 'dia_horas': dia_hora})


def delete_dia_hora(request, id):
    try:
        dia_hora = DiaHora.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        dia_hora.delete()
        messages.success(request, 'Horario eliminado correctamente.')

    return redirect('list_dia_horas')

# ---------------------VISTA ETIQUETA --------------------------------



def list_etiquetas(request):
    etiqueta = Etiqueta.objects.all()
    return render(request, 'etiquetas.html', {'etiquetas': etiqueta})


def create_etiqueta(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioEtiqueta(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta creada correctamente.')
            return redirect('list_etiquetas')

        messages.error(request, 'Error al crear la etiqueta.')
    else:
        form = FomularioEtiqueta()

    return render(request, 'etiquetas-form.html', {'form': form})


def update_etiqueta(request, id):
    try:
        etiqueta = Etiqueta.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioEtiqueta(request.POST, request.FILES, instance=etiqueta)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta actualizada correctamente.')
            return redirect('list_etiquetas')
        messages.error(request, 'Error al modificar Etiqueta.')
    else:
        form = FomularioEtiqueta(instance=etiqueta)

    return render(request, 'etiquetas-form.html', {'form': form, 'etiquetas': etiqueta})


def delete_etiqueta(request, id):
    try:
        etiqueta = Etiqueta.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        etiqueta.delete()
        messages.success(request, 'Etiqueta eliminada correctamente.')

    return redirect('list_etiquetas')

# ---------------------VISTA ETIQUETA_CLASE --------------------------------
def list_etiquetas_clase(request):
    etiqueta_clase = EtiquetaClase.objects.all()
    return render(request, 'etiqueta_clases.html', {'etiquetas_clases': etiqueta_clase})


def create_etiquetas_clase(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioEtiquetaClase(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta_Clase creada correctamente.')
            return redirect('list_etiquetas_clase')

        messages.error(request, 'Error al crear la etiqueta_clase.')
    else:
        form = FomularioEtiquetaClase()

    return render(request, 'etiqueta_clases.html', {'form': form})


def update_etiquetas_clase(request, id):
    try:
        etiqueta_clase = EtiquetaClase.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioEtiquetaClase(request.POST, request.FILES, instance=etiqueta_clase)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta_Clase actualizada correctamente.')
            return redirect('list_etiquetas_clase')
        messages.error(request, 'Error al modificar Etiqueta_Clase.')
    else:
        form = FomularioEtiquetaClase(instance=etiqueta_clase)

    return render(request, 'etiqueta_clases-form.html', {'form': form, 'etiquetas_clases': etiqueta_clase})


def delete_etiquetas_clase(request, id):
    try:
        etiqueta_clase = EtiquetaClase.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        etiqueta_clase.delete()
        messages.success(request, 'Etiqueta_Clase eliminada correctamente.')

    return redirect('list_etiquetas_clase')

# ---------------------VISTA ETIQUETA_GRUPO --------------------------------

def list_etiquetas_grupo(request):
    etiqueta_grupo = EtiquetaGrupo.objects.all()
    return render(request, 'etiqueta_grupos.html', {'etiquetas_grupos': etiqueta_grupo})


def create_etiquetas_grupo(request):
    print(request.method)
    if request.method == 'POST':

        form = FomularioEtiquetaGrupo(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta_Grupo creada correctamente.')
            return redirect('list_etiquetas_grupo')

        messages.error(request, 'Error al crear la etiqueta_clase.')
    else:
        form = FomularioEtiquetaGrupo()

    return render(request, 'etiqueta_grupos.html', {'form': form})


def update_etiquetas_grupo(request, id):
    try:
        etiqueta_grupo = EtiquetaGrupo.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioEtiquetaGrupo(request.POST, request.FILES, instance=etiqueta_grupo)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta_Grupo actualizada correctamente.')
            return redirect('list_etiquetas_grupo')
        messages.error(request, 'Error al modificar Etiqueta_Grupo.')
    else:
        form = FomularioEtiquetaGrupo(instance=etiqueta_grupo)

    return render(request, 'etiqueta_grupos-form.html', {'form': form, 'etiquetas_grupos': etiqueta_grupo})


def delete_etiquetas_grupo(request, id):
    try:
        etiqueta_grupo = EtiquetaGrupo.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        etiqueta_grupo.delete()
        messages.success(request, 'Etiqueta_Grupo eliminada correctamente.')

    return redirect('list_etiquetas_grupo')
# ---------------------VISTA INSCRIPCION --------------------------------

def list_inscripciones(request):
    inscripcion = Inscripcion.objects.all()
    return render(request, 'inscripciones.html', {'inscripciones': inscripcion})


def create_inscripcion(request):
    print(request.method)
    form_inscripcion = FomularioInscripcion()
    form_titular = TitularForm()
    form_alumno = AlumnoForm()
    # del form_alumno.fields['titular_cuenta']

    return render(request, 'inscripciones-form.html', {
        'formInscripcion': form_inscripcion,
        'formTitular': form_titular,
        'formAlumno': form_alumno
    })


def update_inscripcion(request, id):
    try:
        inscripcion = Inscripcion.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FomularioInscripcion(request.POST, request.FILES, instance=inscripcion)

        if form.is_valid():
            form.save()
            messages.success(request, 'Inscripcion actualizada correctamente.')
            return redirect('list_inscripciones')
        messages.error(request, 'Error al modificar Incripcion.')
    else:
        form = FomularioInscripcion(instance=inscripcion)

    return render(request, 'inscripciones-form.html', {'form': form, 'inscripciones': inscripcion})


def delete_inscripcion(request, id):
    try:
        inscripcion = Inscripcion.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        inscripcion.delete()
        messages.success(request, 'inscripcion eliminada correctamente.')

    return redirect('list_inscripciones')


# ---------------------VISTA ASISTENCIA --------------------------------

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
