import datetime

from django.db import models
import sys


# Create your models here.
class Alumno(models.Model):
        cedula = models.CharField(max_length=8, unique=True)
        nombre = models.CharField(max_length=50)
        apellido = models.CharField(max_length=50)
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=50)
        fecha_nacimiento = models.DateField(default=datetime.date.today)
        imagen = models.ImageField(upload_to='media_root', verbose_name='Imagen')
        ficha = models.FileField(upload_to = 'media_root')

        def __str__(self):
            return self.nombre

