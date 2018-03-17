from django.db import models

from personas.models import Persona


class Cuenta(models.Model):
    id_persona = models.ForeignKey(Persona, models.CASCADE)
    descripcion = models.CharField(max_length=100)
    monto = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)

    def __str__(self):
        return self.Persona.nombre
