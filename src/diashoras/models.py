from django.db import models

from grupos.models import Grupo


# Create your models here.

class DiaHora(models.Model):
    DIA = (('L', 'Lunes'),
           ('M', 'Martes'),
           ('X', 'Miercoles'),
           ('J', 'Jueves'),
           ('V', 'Viernes')
           )

    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    dia = models.CharField(max_length=1, choices=DIA)
    hora = models.TimeField()

    def __str__(self):
        return self.id_grupo
