import datetime

from django.db import models

from alumnos.models import Alumno
from grupos.models import Grupo


class Asistencia(models.Model):
    id_alumno = models.ForeignKey(Alumno, models.CASCADE)
    id_grupo = models.ForeignKey(Grupo, models.CASCADE)
    fecha = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.Alumno.nombre
