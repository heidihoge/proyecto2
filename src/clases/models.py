from django.db import models


# Create your models here.
class Clase(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    costo = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre
