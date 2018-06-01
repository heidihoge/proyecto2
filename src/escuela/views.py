from __future__ import unicode_literals

import json
from datetime import datetime

from dal import autocomplete
from django import forms
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.db import connection
from django.template import context, RequestContext

from escuela.utils import dictfetch
from main.forms import TitularForm, AlumnoForm, TitularFormVerificar, AlumnoFormVerificar
from main.models import Alumno, Persona, Titular
from proyecto2 import settings
from tienda.models import VentaCabecera

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


from .forms import FormularioClase,FormularioGrupo, FormularioAsistencia, FomularioEtiqueta, FomularioEtiquetaClase, FormularioEtiquetaGrupo, FormularioInscripcion
from .models import Clase, Grupo, Etiqueta, EtiquetaGrupo, EtiquetaClase, Inscripcion, Asistencia, Cuenta


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

        form = FormularioClase(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Clase creada correctamente.')
            return redirect('list_clases')

        messages.error(request, 'Error al crear la clase.')
    else:
        form = FormularioClase()

    return render(request, 'clases-form.html', {'form': form})


def update_clase(request, id):
    try:
        clase = Clase.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FormularioClase(request.POST, request.FILES, instance=clase)

        if form.is_valid():
            form.save()
            messages.success(request, 'Clase actualizada correctamente.')
            return redirect('list_clases')
        messages.error(request, 'Error al modificar Clase.')
    else:
        form = FormularioClase(instance=clase)

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

        form = FormularioGrupo(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo creada correctamente.')
            return redirect('list_grupos')

        messages.error(request, 'Error al crear el grupo.')
    else:
        form = FormularioGrupo()

    return render(request, 'grupos-form.html', {'form': form})


def update_grupo(request, id):
    try:
        grupo = Grupo.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FormularioGrupo(request.POST, request.FILES, instance=grupo)

        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo actualizado correctamente.')
            return redirect('list_grupos')
        messages.error(request, 'Error al modificar Grupo.')
    else:
        form = FormularioGrupo(instance=grupo)

    return render(request, 'grupos-form.html', {'form': form, 'clase': grupo})


def delete_grupo(request, id):
    try:
        grupo = Grupo.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        try:
            grupo.delete()
            messages.success(request, 'Grupo eliminado correctamente.')
        except:
            messages.error(request, 'No puedes borrar el grupo, está siendo utilizado')

    return redirect('list_grupos')


# # ---------------------VISTA DIA_HORA --------------------------------
# def list_dia_horas(request):
#     dia_hora = DiaHora.objects.all()
#     return render(request, 'dia_horas.html', {'dia_horas': dia_hora})
#
#
# def create_dia_hora(request):
#     print(request.method)
#     if request.method == 'POST':
#
#         form = FomularioDiaHora(request.POST, request.FILES)
#
#         if form.is_valid():
#
#             grupo_id = request.POST['grupo_id']
#             grupo = Grupo.objects.get(id=int(grupo_id))
#             form.instance.grupo = grupo
#             form.save()
#             messages.success(request, 'Dia_hora creada correctamente.')
#             return redirect('list_dia_horas')
#
#         messages.error(request, 'Error al crear dias y horas.')
#     else:
#         form = FomularioDiaHora()
#
#     return render(request, 'dia_horas-form.html', {'form': form})
#
#
# def update_dia_hora(request, id):
#     try:
#         dia_hora = DiaHora.objects.get(id=id)
#     except:
#         return redirect('404')
#     if request.method == 'POST':
#         form = FomularioDiaHora(request.POST, request.FILES, instance=dia_hora)
#
#         if form.is_valid():
#
#             grupo_id = request.POST['grupo_id']
#             grupo = Grupo.objects.get(id=int(grupo_id))
#             form.instance.grupo = grupo
#
#             form.save()
#             messages.success(request, 'DIA Y HORA actualizado correctamente.')
#             return redirect('list_dia_horas')
#         messages.error(request, 'Error al modificar DIA Y HORA.')
#     else:
#         form = FomularioDiaHora(instance=dia_hora, initial={'grupo_id': dia_hora.grupo_id})
#
#     return render(request, 'dia_horas-form.html', {'form': form, 'dia_horas': dia_hora})
#
#
# def delete_dia_hora(request, id):
#     try:
#         dia_hora = DiaHora.objects.get(id=id)
#     except:
#         return redirect('404')
#
#     if request.method == 'POST':
#         dia_hora.delete()
#         messages.success(request, 'Horario eliminado correctamente.')
#
#     return redirect('list_dia_horas')

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

        form = FormularioEtiquetaGrupo(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta_Grupo creada correctamente.')
            return redirect('list_etiquetas_grupo')

        messages.error(request, 'Error al crear la etiqueta_clase.')
    else:
        form = FormularioEtiquetaGrupo()

    return render(request, 'etiqueta_grupos.html', {'form': form})


def update_etiquetas_grupo(request, id):
    try:
        etiqueta_grupo = EtiquetaGrupo.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = FormularioEtiquetaGrupo(request.POST, request.FILES, instance=etiqueta_grupo)

        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta_Grupo actualizada correctamente.')
            return redirect('list_etiquetas_grupo')
        messages.error(request, 'Error al modificar Etiqueta_Grupo.')
    else:
        form = FormularioEtiquetaGrupo(instance=etiqueta_grupo)

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
    form_inscripcion = FormularioInscripcion()
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
        form = FormularioInscripcion(request.POST, request.FILES, instance=inscripcion)

        if form.is_valid():
            form.save()
            messages.success(request, 'Inscripcion actualizada correctamente.')
            return redirect('list_inscripciones')
        messages.error(request, 'Error al modificar Incripcion.')
    else:
        form = FormularioInscripcion(instance=inscripcion)

    return render(request, 'inscripciones-form.html', {'form': form, 'inscripciones': inscripcion})

@login_required()
@permission_required('escuela.inscripcion_baja', raise_exception=True)
# lista para dar de baja , debe traer solo los activos
def list_inscripciones_baja(request):
    inscripcion = Inscripcion.objects.filter(estado='A')
    return render(request, 'inscripciones-bajas.html', {'inscripciones': inscripcion})



import datetime
def baja_inscripcion(request, id):

    try:
        inscripcion = Inscripcion.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        hoy = datetime.now()
        inscripcion.fecha_fin = hoy
        inscripcion.estado = 'IN'
        inscripcion.save()

        messages.success(request, 'inscripcion dado de baja correctamente.')

    return redirect('list_inscripciones_baja')


# ---------------------VISTA ASISTENCIA --------------------------------


def lista_asistencia(request):
    def alumno_json(alumno):

        grupo = Grupo(lunes=alumno['lunes'], martes=alumno['martes'], miercoles=alumno['miercoles'],
                      jueves=alumno['jueves'], viernes=alumno['viernes'], sabado=alumno['sabado'],
                      domingo=alumno['domingo'])
        nombre_grupo = "{0} ({1}) Dias: ({2}) - Horario: ({3} - {4})".format(alumno["clase_nombre"],
                                                                             alumno["profesor_nombre"],
                                                                             grupo.get_dias(),
                                                                             format(alumno['hora_inicio'], '%H:%M'),
                                                                             format(alumno['hora_fin'], '%H:%M'))
        return {
            "id": alumno["alumno_id"],
            "nombre": alumno["alumno_nombre"],
            "grupo": {
                "id": alumno["id"], # es id de grupo
                "nombre": nombre_grupo
            },
            "asistencia_presente": alumno["asistencia_presente"],
            "asistencia_id": alumno["asistencia_id"],
            "asistencia_comentario": alumno["asistencia_comentario"],
            "inscripcion_vencida": alumno["inscripcion_vencida"]
        }

    ret = {}
    if request.method == 'GET':
        fecha = request.GET.get('fecha')
        fecha = datetime.strptime(fecha, settings.DATE_INPUT_FORMATS[0]).date()
        # .strftime(settings.DATE_INPUT_FORMATS[0])
        grupo = request.GET.get('grupo')
        # Obtener alumnos
        query = '''
            SELECT distinct
                p.id as alumno_id,
                p.nombre::text || ' ' || p.apellido::text || ' (' || p.cedula::text || ')' as alumno_nombre,
                g.*,
                prof.nombre::text || ' ' || prof.apellido::text as profesor_nombre,
                c.nombre as clase_nombre,
                asis.id as asistencia_id,
                asis.presente as asistencia_presente,
                COALESCE(asis.comentario, '') as asistencia_comentario,
                COALESCE(i.fecha_fin <= %(fecha)s, FALSE) as inscripcion_vencida
            FROM main_alumno a
              JOIN main_persona p ON a.persona_ptr_id = p.id
              JOIN escuela_inscripcion i ON a.persona_ptr_id = i.alumno_id AND
                                          i.fecha_inicio <= %(fecha)s AND i.estado = 'A'
                                         -- AND (i.fecha_fin >= %(fecha)s OR i.fecha_fin IS NULL)
              JOIN escuela_grupo g ON i.grupo_id = g.id
              JOIN escuela_clase c ON c.id = g.id_clase_id
              JOIN main_persona prof ON g.id_profesor_id = prof.id
              LEFT JOIN escuela_asistencia asis
                ON g.id = asis.grupo_id AND asis.fecha = %(fecha)s  AND asis.id_alumno_id = a.persona_ptr_id
        '''

        dia = fecha.weekday()
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

        query += " WHERE g.{0} = true ".format(dias[dia])

        if grupo and grupo != '-1':
            grupo = int(grupo)
            query += " AND g.id = %(grupo)s"
        cursor = connection.cursor()
        cursor.execute(query, {"fecha": fecha, "grupo": grupo})
        ret = dictfetch(cursor, 100, 0)
        ret = {
            "dia": fecha,
            "grupo": grupo,
            "alumnos": list(map(alumno_json, ret))
        }

    return JsonResponse(ret, safe=False)

def guardar_inscripcion(request):
    if request.method == 'POST':
        titular = None
        errores = []
        if 'cedula' in request.POST:
            cedula = request.POST['cedula']
            try:
                titular = Titular.objects.get(cedula=cedula)
            except Exception as e1:
                try:
                    persona = Persona.objects.get(cedula=cedula)
                    titular = Titular(persona_ptr_id=persona.pk)
                    titular.__dict__.update(persona.__dict__)
                except  Exception as e2:
                    titular = Titular()

        form = TitularFormVerificar(request.POST, request.FILES, instance=titular)
        if form.is_valid():
            titular = form.save()
        else:
            errores.append(1)


        cantidad_alumnos = int(request.POST['alumnosCount'])

        for i in range(1, cantidad_alumnos + 1):
            prefix = 'alumno-' + str(i)
            alumno = None
            if prefix + '-cedula' in request.POST:
                cedula = request.POST[prefix + '-cedula']
                try:
                    alumno = Alumno.objects.get(cedula=cedula)
                except Exception as e1:
                    try:
                        persona = Persona.objects.get(cedula=cedula)
                        alumno = Alumno(persona_ptr_id=persona.pk)
                        alumno.__dict__.update(persona.__dict__)
                    except Exception as e2:
                        alumno = Alumno()

            alumno.titular_cuenta = titular
            form = AlumnoFormVerificar(request.POST, request.FILES, instance=alumno, prefix=prefix)
            if form.is_valid():
                alumno = form.save()
            else:
                errores.append(2)


            prefix = 'alumno-' + str(i) + '-inscripcion'
            if prefix + '-grupo' in request.POST:
                grupo = request.POST[prefix + '-grupo']
                try:
                    inscripcion = Inscripcion.objects.get(alumno=alumno, grupo_id=grupo)
                    inscripcion.fecha_fin = None
                except Exception as e1:
                    inscripcion = Inscripcion()

            form = FormularioInscripcion(request.POST, prefix=prefix, instance=inscripcion)

            if form.is_valid() and alumno:
                inscripcion = form.save(commit=False)
                inscripcion.alumno = alumno
                inscripcion.save()
            else:
                errores.append(3)

            if not errores:
                cuenta = Cuenta(inscripcion=inscripcion, vencimiento=inscripcion.fecha_inicio,
                                monto=inscripcion.grupo.costo)
                cuenta.save()

        if len(errores) == 0:
            messages.success(request, 'Inscripcion guardada correctamente.')

        return JsonResponse({"errores": errores}, safe=False)
    raise Http404()

def create_asistencia(request):
    print(request.method)
    if request.method == 'POST':

        form = FormularioAsistencia(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia creada correctamente.')
            return redirect('home')

        messages.error(request, 'Error al crear asistencia.')
    else:
        form = FormularioAsistencia()

    return render(request, 'asistencias-form.html', {'form': form})


def update_asistencia(request):
    if request.method == 'POST':

        alumnos = json.loads(request.body)
        for alumno in alumnos:
            asistencia, _ = Asistencia.objects.get_or_create(id_alumno_id=alumno['alumno_id'],
                                                          grupo_id=alumno['grupo_id'],
                                                          fecha=datetime.strptime(alumno['fecha'],
                                                                                  settings.DATE_INPUT_FORMATS[0]).date())
            asistencia.presente = True if alumno['asistencia_presente'] else False
            asistencia.comentario = alumno['asistencia_comentario']
            asistencia.save()

        return HttpResponse(status=200)


    return HttpResponse(status=400)




class GrupoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Grupo.objects.none()

        qs = Grupo.objects.all()

        if self.q:
            qs = qs.filter(Q(id_clase__nombre__istartswith=self.q) | Q(id_profesor__nombre__istartswith=self.q) \
                           | Q(id_profesor__apellido__istartswith=self.q))

        return qs

class GrupoAutocompleteAsistencia(GrupoAutocomplete):
    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        results = [{
                'id': result.pk,
                'text': self.get_result_label(result),
                'pk': result.pk,
            } for result in context['object_list']]
        return [
            {
                'id': '-1',
                'text': 'Todos los grupos',
                'pk': '-1'
            },
            *results
        ]



# ----------VISTA DE CUENTAS ----------------------------------------

def list_cuentas(request):

    cuenta = Cuenta.objects.all()
    return render(request, 'cuentas.html', {'cuentas': cuenta})


from datetime import datetime

def a_view(request):
    return render_to_response("cuentas.html", {
        'hoy':datetime.now(),
        })
    # else:
    #    return False


