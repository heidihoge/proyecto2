from django.db import models


# Create your models here.

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, primary_key=True)
    descripcion = models.CharField(max_length=100)
    color = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre
