import datetime

from django.db import models

# Create your models here.
from main.models import Alumno, Cuenta, Profesor, Persona, Empleado


# clase

class Clase(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    costo = models.IntegerField(default=0)

    def __str__(self):
        return  self.objects

# grupo


class Grupo(models.Model):
    id_clase = models.ForeignKey(Clase, on_delete=models.SET_NULL,null=True)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL,null=True)
    cupo_maximo = models.IntegerField(default=0)
    costo = models.IntegerField(default=0)

    def __str__(self):
        return self.costo + self.cupo_maximo


# dia_hora

class DiaHora(models.Model):
    DIA = (('L', 'Lunes'),
           ('M', 'Martes'),
           ('X', 'Miercoles'),
           ('J', 'Jueves'),
           ('V', 'Viernes')
           )

    id_grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    dia = models.CharField(max_length=1, choices=DIA)
    hora = models.TimeField()

    def __str__(self):
        return self.objects

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
        return self.objects

# etiqueta_grupo

class EtiquetaGrupo(models.Model):
    id_grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.objects

# inscripcion

class Inscripcion(models.Model):
    id_grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    id_alumno = models.ForeignKey(Alumno,on_delete=models.SET_NULL,null=True)
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.objects

# asistencia

class Asistencia(models.Model):
    id_alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL,null=True)
    id_grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    fecha = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.objects
