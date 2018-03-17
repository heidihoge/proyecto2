from django.db import models

from clases.models import Clase
from profesores.models import Profesor


# Create your models here.

class Grupo(models.Model):
    id_clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    cupo_maximo = models.IntegerField(default=0)
    costo = models.IntegerField(default=0)

    def __str__(self):
        return self.Clase.nombre
