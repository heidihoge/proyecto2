from __future__ import unicode_literals
from django.shortcuts import render

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
