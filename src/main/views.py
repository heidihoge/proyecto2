import json

import datetime
from _dummy_thread import error

from dal import autocomplete
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, Http404
from django.db.models import Q

# Create your views here.
from escuela.forms import FormularioInscripcion
from escuela.models import Inscripcion
from proyecto2 import settings


@login_required
def index(request):
    return render(request, 'index.html', context={})


def login(request):
    return render(request, 'login.html', context={})


def redirect_to_index(request):
    return redirect('/')

@login_required
def error404(request):
    return render(request, 'errors/page_404.html', context={})


def error403(request):
    return render(request, '403.html', context={})


# ---------------------VISTA PERSONAS --------------------------------

from django.contrib import messages
from django.shortcuts import render, redirect


class ProfesorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Profesor.objects.none()

        qs = Profesor.objects.all()

        if self.q:
            qs = qs.filter(Q(nombre__istartswith=self.q) | Q(cedula__isstartwith=self.q) | Q(apellido__istartswith=self.q))

        return qs


class AlumnoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Alumno.objects.none()

        qs = Alumno.objects.all()

        if self.q:
            qs = qs.filter(Q(cedula__istartswith=self.q) | Q(apellido__istartswith=self.q))

        return qs

    def _get_fields_as_json(self, result):
        # return json.loads(serializers.serialize('json', [result]))[0]['fields']
        result = result.__dict__
        del result['_state']
        if isinstance(result['fecha_nacimiento'], datetime.date):
            result['fecha_nacimiento'] = result['fecha_nacimiento'].strftime(settings.DATE_INPUT_FORMATS[0])
        return result

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': result.pk,
                'text': str(result.cedula) + ' (' + self.get_result_label(result) + ')',
                'pk': result.pk,
                'fields': self._get_fields_as_json(result)
            } for result in context['object_list']
        ]


class PersonaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Persona.objects.none()

        qs = Persona.objects.all()

        if self.q:
            qs = qs.filter(Q(cedula__istartswith=self.q) | Q(apellido__istartswith=self.q)| Q(nombre__istartswith=self.q))

        return qs

    def _get_fields_as_json(self, result):
        # return json.loads(serializers.serialize('json', [result]))[0]['fields']
        result = result.__dict__
        del result['_state']
        if isinstance(result['fecha_nacimiento'], datetime.date):
            result['fecha_nacimiento'] = result['fecha_nacimiento'].strftime(settings.DATE_INPUT_FORMATS[0])
        return result

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': result.cedula,
                'text': self.get_result_label(result),
                'pk': result.pk,
                'fields': self._get_fields_as_json(result)
            } for result in context['object_list']
        ]


from .forms import PersonaForm, TitularFormVerificar, AlumnoFormVerificar
from .models import Persona

@login_required() #permisos para login
def list_personas(request):
    persona = Persona.objects.all()
    return render(request, 'main/personas.html', {'personas': persona})

@login_required() #permisos para login
def create_persona(request):
    print(request.method)
    if request.method == 'POST':

        form = PersonaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Persona creada correctamente.')
            return redirect('list_personas')

        messages.error(request, 'Error al crear la personas.')
    else:
        form = PersonaForm()

    return render(request, 'main/personas-form.html', {'form': form})

@login_required() #permisos para login
def update_persona(request, id):
    try:
        persona = Persona.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES, instance=persona)

        if form.is_valid():
            form.save()
            messages.success(request, 'Persona actualizada correctamente.')
            return redirect('list_personas')
        messages.error(request, 'Error al modificar Persona.')
    else:
        form = PersonaForm(instance=persona)

    return render(request, 'main/personas-form.html', {'form': form, 'persona': persona})

@login_required() #permisos para login
def delete_persona(request, id):
    try:
        persona = Persona.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        persona.delete()
        messages.success(request, 'Persona eliminada correctamente.')

    return redirect('list_personas')


# ---------------------VISTA TITULAR --------------------------------

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import TitularForm
from .models import Titular


@login_required() #permisos para login
#@permission_required('titular_list', raise_exception=True)
def list_titulares(request):
    titular = Titular.objects.all()
    return render(request, 'main/titulares.html', {'titulares': titular})


@login_required() #permisos para login
def verificar_titular(request):
    if request.method == 'POST':
        titular = None
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
                    titular = None

        form = TitularFormVerificar(request.POST, request.FILES, instance=titular)
        return JsonResponse({"valid": form.is_valid(), "errors": form.errors})
    raise Http404()


@login_required() #permisos para login
def verificar_alumnos(request):
    if request.method == 'POST':
        cantidad_alumnos = int(request.POST['alumnosCount'])
        alumnos = []
        for i in range(1, cantidad_alumnos + 1):
            prefix = 'alumno-' + str(i)
            alumno = None
            if prefix + '-cedula' in request.POST:
                cedula = request.POST[prefix + '-cedula']
                try:
                    alumno = Persona.objects.get(cedula=cedula)
                except:
                    alumno = None

            form = AlumnoFormVerificar(request.POST, request.FILES, instance=alumno, prefix=prefix)
            alumnos.append({"alumno": i, "valid": form.is_valid(), "errors": form.errors})

        return JsonResponse(alumnos, safe=False)
    raise Http404()


@login_required() #permisos para login
def cargar_cupo(cupos, grupo):
    if grupo not in cupos:
        inscriptos = Inscripcion.objects.filter(Q(grupo=grupo) & Q(fecha_fin__isnull=True)).count()
        cupos[grupo] = grupo.cupo_maximo - inscriptos


@login_required() #permisos para login
def verificar_inscripcion(request):
    if request.method == 'POST':
        cantidad_alumnos = int(request.POST['alumnosCount'])
        inscripciones = []
        cupos = {}
        for i in range(1, cantidad_alumnos + 1):
            prefix = 'alumno-' + str(i) + '-inscripcion'
            form = FormularioInscripcion(request.POST, prefix=prefix)
            form.is_valid()
            error_cupos = None
            if 'grupo' in form.cleaned_data:
                grupo = form.cleaned_data['grupo']
                cargar_cupo(cupos, grupo)
                cupos[grupo] = cupos[grupo] - 1
                if cupos[grupo] < 0:
                    error_cupos = "Grupo lleno."
            inscripciones.append({"alumno": i, "valid": form.is_valid(),
                                  "errors": form.errors, "error_cupos": error_cupos})

        return JsonResponse(inscripciones, safe=False)
    raise Http404()


@login_required() #permisos para login
#@permission_required('titular_create', raise_exception=True)
def create_titular(request):
    print(request.method)
    if request.method == 'POST':

        form = TitularFormVerificar(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Titular creado correctamente.')
            return redirect('list_titulares')

        form = TitularForm(request.POST, request.FILES)
        messages.error(request, 'Error al crear el titular.')
    else:
        form = TitularForm()

    return render(request, 'main/titulares-form.html', {'form': form})


@login_required() #permisos para login
#@permission_required('titular_update', raise_exception=True)
def update_titular(request, id):
    try:
        titular = Titular.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = TitularForm(request.POST, request.FILES, instance=titular)

        if form.is_valid():
            form.save()
            messages.success(request, 'Titular actualizado correctamente.')
            return redirect('list_titulares')
        messages.error(request, 'Error al modificar Titular.')
    else:
        form = PersonaForm(instance=titular)

    return render(request, 'main/titulares-form.html', {'form': form, 'titular': titular})

@login_required()
@permission_required('titular_delete', raise_exception=True)

@transaction.non_atomic_requests
def delete_titular(request, id):
    try:
        titular = Titular.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        try:
            with transaction.atomic():
                titular.delete()
            messages.success(request, 'Titular eliminado correctamente.')
        except Exception as e:
            messages.error(request, 'El Titular no puede ser eliminado, está siendo utilizado.')

    return redirect('list_titulares')






# ---------------------VISTA ALUMNOS --------------------------------
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import AlumnoForm
from .models import Alumno


@login_required() #permisos para login
#@permission_required('main.alumno_list', raise_exception=True)
def list_alumnos(request):
    alumno = Alumno.objects.all()
    return render(request, 'main/alumnos.html', {'alumnos': alumno})


@login_required() #permisos para login
#@permission_required('main.alumno_create', raise_exception=True)
def create_alumno(request):
    print(request.method)
    if request.method == 'POST':

        form = AlumnoFormVerificar(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno creado correctamente.')
            return redirect('list_alumnos')

        form = AlumnoForm(request.POST, request.FILES)
        messages.error(request, 'Error al crear el alumno.')
    else:
        form = AlumnoForm()

    return render(request, 'main/alumnos-form.html', {'form': form})


@login_required() #permisos para login
#@permission_required('main.alumno_update', raise_exception=True)
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
        messages.error(request, 'Error al modificar Alumno.')
    else:
        form = AlumnoForm(instance=alumno)

    return render(request, 'main/alumnos-form.html', {'form': form, 'alumno': alumno})


@login_required() #permisos para login
@permission_required('alumno_delete', raise_exception=True)
@transaction.non_atomic_requests
def delete_alumno(request, id):
    try:
        alumno = Alumno.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        try:
            with transaction.atomic():
                alumno.delete()
            messages.success(request, 'alumno eliminado correctamente.')
        except Exception as e:
            messages.error(request, 'El alumno no puede ser eliminado, está siendo utilizado.')

    return redirect('list_alumnos')



# ---------------------VISTA EMPLEADOS --------------------------------
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import EmpleadoForm
from .models import Empleado


def list_empleados(request):
    empleado = Empleado.objects.all()
    return render(request, 'main/empleados.html', {'empleados': empleado})

@login_required() #permisos para login
@permission_required('main.empleado_create', raise_exception=True)
def create_empleado(request):
    print(request.method)
    if request.method == 'POST':

        form = EmpleadoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado correctamente.')
            return redirect('list_empleados')

        messages.error(request, 'Error al crear empleado.')
    else:
        form = EmpleadoForm()

    return render(request, 'main/empleados-form.html', {'form': form})

@login_required() #permisos para login
@permission_required('main.empleado_update', raise_exception=True)
def update_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)

        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('list_empleados')
        messages.error(request, 'Error al modificar Empleado.')
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'main/empleados-form.html', {'form': form, 'empleado': empleado})

@login_required() #permisos para login
@permission_required('main.empleado_delete', raise_exception=True)

@transaction.non_atomic_requests
def delete_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        try:
            with transaction.atomic():
                empleado.delete()
            messages.success(request, 'empleado eliminado correctamente.')
        except Exception as e:
            messages.error(request, 'El empleado no puede ser eliminado, está siendo utilizado.')

    return redirect('list_empleados')

# ---------------------VISTA PROFESORES --------------------------------
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ProfesorForm
from .models import Profesor

@login_required() #permisos para login
#@permission_required('main.profesor_list', raise_exception=True)
def list_profesores(request):
    profesor = Profesor.objects.all()
    return render(request, 'main/profesores.html', {'profesores': profesor})


@login_required() #permisos para login
@permission_required('main.profesor_create', raise_exception=True)
def create_profesor(request):
    print(request.method)
    if request.method == 'POST':

        form = ProfesorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profesor creado correctamente.')
            return redirect('list_profesores')

        messages.error(request, 'Error al crear profesor.')
    else:
        form = ProfesorForm()

    return render(request, 'main/profesores-form.html', {'form': form})


@login_required() #permisos para login
@permission_required('main.profesor_update', raise_exception=True)
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
        messages.error(request, 'Error al modificar Profesor.')
    else:
        form = ProfesorForm(instance=profesor)

    return render(request, 'main/profesores-form.html', {'form': form, 'profesor': profesor})

@login_required() #permisos para login
@permission_required('main.profesor_delete', raise_exception=True)
@transaction.non_atomic_requests
def delete_profesor(request, id):
    try:
        profesor = Profesor.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        try:
            with transaction.atomic():
                profesor.delete()
            messages.success(request, 'profesor eliminado correctamente.')
        except Exception as e:
            messages.error(request, 'El profesor no puede ser eliminado, está siendo utilizado.')

    return redirect('list_profesores')


# ---------------------VISTA CUENTAS --------------------------------
from django.contrib import messages
from django.shortcuts import render, redirect

