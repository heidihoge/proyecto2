import json

import datetime
from _dummy_thread import error

from dal import autocomplete
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect, Http404
from django.db.models import Q

# Create your views here.
from escuela.forms import FormularioInscripcion
from proyecto2 import settings


@login_required
def index(request):
    return render(request, 'index.html', context={})


def login(request):
    return render(request, 'login.html', context={})


def redirect_to_index(request):
    return redirect('/')


def error404(request):
    return render(request, 'errors/page_404.html', context={})


def error403(request):
    return render(request, 'errors/page_403.html', context={})


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
            qs = qs.filter(Q(nombre__istartswith=self.q) | Q(cedula__isstartwith=self.q))

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
                'id': result.cedula,
                'text': str(result.cedula) + ' (' + self.get_result_label(result) + ')',
                'pk': result.pk,
                'fields': self._get_fields_as_json(result)
            } for result in context['object_list']
        ]


from .forms import PersonaForm
from .models import Persona


def list_personas(request):
    persona = Persona.objects.all()
    return render(request, 'main/personas.html', {'personas': persona})


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


def list_titulares(request):
    titular = Titular.objects.all()
    return render(request, 'main/titulares.html', {'titulares': titular})


def verificar_titular(request):
    if request.method == 'POST':
        titular = None
        if 'cedula' in request.POST:
            cedula = request.POST['cedula']
            try:
                titular = Persona.objects.get(cedula=cedula)
            except:
                titular = None

        form = TitularForm(request.POST, request.FILES, instance=titular)
        return JsonResponse({"valid": form.is_valid(), "errors": form.errors})
    raise Http404()


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

            form = AlumnoForm(request.POST, request.FILES, instance=alumno, prefix=prefix)
            alumnos.append({"alumno": i, "valid": form.is_valid(), "errors": form.errors})

        return JsonResponse(alumnos, safe=False)
    raise Http404()


def verificar_inscripcion(request):
    if request.method == 'POST':
        cantidad_alumnos = int(request.POST['alumnosCount'])
        inscripciones = []
        for i in range(1, cantidad_alumnos + 1):
            prefix = 'alumno-' + str(i) + '-inscripcion'
            form = FormularioInscripcion(request.POST, prefix=prefix)
            inscripciones.append({"alumno": i, "valid": form.is_valid(), "errors": form.errors})

        return JsonResponse(inscripciones, safe=False)
    raise Http404()


@permission_required('add_titular', raise_exception=True)
def create_titular(request):
    print(request.method)
    if request.method == 'POST':

        form = TitularForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Titular creado correctamente.')
            return redirect('list_titulares')

        messages.error(request, 'Error al crear el titular.')
    else:
        form = TitularForm()

    return render(request, 'main/titulares-form.html', {'form': form})


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


def delete_titular(request, id):
    try:
        titular = Titular.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        titular.delete()
        messages.success(request, 'Titular eliminado correctamente.')

    return redirect('list_titulares')


# ---------------------VISTA ALUMNOS --------------------------------
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import AlumnoForm
from .models import Alumno


def list_alumnos(request):
    alumno = Alumno.objects.all()
    return render(request, 'main/alumnos.html', {'alumnos': alumno})


def create_alumno(request):
    print(request.method)
    if request.method == 'POST':

        form = AlumnoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno creado correctamente.')
            return redirect('list_alumnos')

        messages.error(request, 'Error al crear el alumno.')
    else:
        form = AlumnoForm()

    return render(request, 'main/alumnos-form.html', {'form': form})


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


def delete_alumno(request, id):
    try:
        alumno = Alumno.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        try:
            alumno.delete()
            messages.success(request, 'Alumno eliminado correctamente.')
        except:
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


def delete_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado correctamente.')

    return redirect('list_empleados')


# ---------------------VISTA PROFESORES --------------------------------
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ProfesorForm
from .models import Profesor


def list_profesores(request):
    profesor = Profesor.objects.all()
    return render(request, 'main/profesores.html', {'profesores': profesor})


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


def delete_profesor(request, id):
    try:
        profesor = Profesor.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        profesor.delete()
        messages.success(request, 'Profesor eliminado correctamente.')

    return redirect('list_profesores')


# ---------------------VISTA CUENTAS --------------------------------
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CuentaForm
from .models import Cuenta


def list_cuentas(request):
    cuenta = Cuenta.objects.all()
    return render(request, 'main/cuentas.html', {'cuentas': cuenta})


def create_cuenta(request):
    print(request.method)
    if request.method == 'POST':

        form = CuentaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creado correctamente.')
            return redirect('list_cuentas')

        messages.error(request, 'Error al crear cuenta.')
    else:
        form = CuentaForm()

    return render(request, 'main/cuentas-form.html', {'form': form})


def update_cuenta(request, id):
    try:
        cuenta = Cuenta.objects.get(id=id)
    except:
        return redirect('404')
    if request.method == 'POST':
        form = CuentaForm(request.POST, request.FILES, instance=cuenta)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta actualizada correctamente.')
            return redirect('list_cuentas')
        messages.error(request, 'Error al modificar Cuenta.')
    else:
        form = ProfesorForm(instance=cuenta)

    return render(request, 'main/cuentas-form.html', {'form': form, 'cuenta': cuenta})


def delete_cuenta(request, id):
    try:
        cuenta = Cuenta.objects.get(id=id)
    except:
        return redirect('404')

    if request.method == 'POST':
        cuenta.delete()
        messages.success(request, 'Cuenta eliminado correctamente.')

    return redirect('list_cuentas')
