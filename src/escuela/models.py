import datetime

from django.db import models

# Create your models here.
from django.shortcuts import render

from main.models import Alumno, Profesor, Persona, Empleado


# clase
from tienda.models import VentaDetalle, VentaCabecera


class Clase(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)


    def __str__(self):
        return  self.nombre

# grupo


class Grupo(models.Model):
    id_clase = models.ForeignKey(Clase, on_delete=models.PROTECT,null=True)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL,null=True)
    cupo_maximo = models.IntegerField(default=0)
    costo = models.IntegerField(default=0)
    lunes = models.BooleanField(default=False, null=False, blank=True)
    martes = models.BooleanField(default=False, null=False, blank=True)
    miercoles = models.BooleanField(default=False, null=False, blank=True)
    jueves = models.BooleanField(default=False, null=False, blank=True)
    viernes = models.BooleanField(default=False, null=False, blank=True)
    sabado = models.BooleanField(default=False, null=False, blank=True)
    domingo = models.BooleanField(default=False, null=False, blank=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def get_dias(self):
        dias = zip(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
                   [self.lunes, self.martes, self.miercoles, self.jueves, self.viernes, self.sabado, self.domingo])
        dias = filter(lambda x: x[1], dias)
        dias = map(lambda x: x[0], dias)
        return ",".join(list(dias))


    def __str__(self):
        return "{0} ({1}) Dias: ({2}) - Horario: ({3} - {4})" \
            .format(self.id_clase.nombre, str(self.id_profesor), self.get_dias(),
                    format(self.hora_inicio, '%H:%M'), format(self.hora_fin, '%H:%M'))

    def grupo_desc(self):
        return "Dias: ({0}) - Horario: ({1} - {2})" \
            .format(self.get_dias(), format(self.hora_inicio, '%H:%M'), format(self.hora_fin, '%H:%M'))

    def short_desc(self):
        return "Clase: {0} Dias: ({1}) Monto: {2}" \
            .format(self.id_clase.nombre,  self.get_dias(),
                    self.costo)


# dia_hora



# etiqueta

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)
    descripcion = models.CharField(max_length=100)
    color = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

# etiqueta_clase

class EtiquetaClase(models.Model):
    id_clase = models.ForeignKey(Clase, on_delete=models.SET_NULL,null=True)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.id_clase

# etiqueta_grupo

class EtiquetaGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.grupo

# inscripcion

class Inscripcion(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT,null=True)
    alumno = models.ForeignKey(Alumno,on_delete=models.SET_NULL,null=True)
    fecha_inicio = models.DateField(default=datetime.date.today, db_index=True)
    fecha_fin = models.DateField(default=None, null=True, db_index=True)
    ESTADO = (('A', 'ACTIVO'),
              ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=2, choices=ESTADO, default='A')

    class Meta:
        permissions = (
            ("inscripcion_baja", "Dar de baja inscripcion"),
        )

# asistencia

class Asistencia(models.Model):
    id_alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL,null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    fecha = models.DateField(default=datetime.date.today, db_index=True)
    presente = models.BooleanField(default=False)
    comentario = models.CharField(max_length=300, default='')

    class Meta:
        unique_together=(('id_alumno','grupo','fecha'),)
    def __str__(self):
        return self.grupo


#Cuenta
class Cuenta(models.Model):
    inscripcion = models.ForeignKey(Inscripcion,on_delete=models.PROTECT)
    vencimiento = models.DateField(default=datetime.date.today)
    monto = models.IntegerField(default=0)
    monto_pagado = models.IntegerField(default=0)
    pagado = models.BooleanField(default=False)
    detalle = models.ForeignKey(VentaDetalle, on_delete=models.PROTECT, null=True)
    referencia = models.CharField(max_length=100 , null=True,blank=True, default='' )

    def __str__(self):
        return "Alumno: {1} {0} Vto: {2}".format(str(self.inscripcion.grupo.short_desc()), str(self.inscripcion.alumno), str(self.vencimiento))

    def vencio(self):
        if self.pagado ==False:
            return self.vencimiento < datetime.date.today()



