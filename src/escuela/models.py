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
        return  self.nombre

# grupo


class Grupo(models.Model):
    id_clase = models.ForeignKey(Clase, on_delete=models.SET_NULL,null=True)
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
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    alumno = models.ForeignKey(Alumno,on_delete=models.SET_NULL,null=True)
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=None, null=True)

    def __str__(self):
        return self.grupo

# asistencia

class Asistencia(models.Model):
    id_alumno = models.ForeignKey(Alumno, on_delete=models.SET_NULL,null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL,null=True)
    fecha = models.DateField(default=datetime.date.today)
    class Meta:
        unique_together=(('id_alumno','grupo','fecha'),)
    def __str__(self):
        return self.grupo
