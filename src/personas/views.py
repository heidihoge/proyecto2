from django.contrib import messages
from django.shortcuts import render, redirect

import personas
from .forms import PersonaForm
from .models import Persona


def list_personas(request):
    persona = Persona.objects.all()
    return render(request, 'personas/personas.html', {'personas': personas})


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

    return render(request, 'personas/personas-form.html', {'form': form})


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

    return render(request, 'personas/personas-form.html', {'form': form, 'persona': persona})


def delete_persona(request, id):
    persona = Persona.objects.get(id=id)

    if request.method == 'POST':
        persona.delete()
        messages.success(request, 'Persona eliminada correctamente.')

    return redirect('list_personas')
