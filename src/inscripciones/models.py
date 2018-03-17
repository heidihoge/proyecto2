import datetime

from django.db import models

from alumnos.models import Alumno
from grupos.models import Grupo


# Create your models here.

class Inscripcion(models.Model):
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.Clase.nombre
