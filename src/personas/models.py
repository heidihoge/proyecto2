import datetime

from django.db import models


# Create your models here.
class Persona(models.Model):
    SEXO = (
        ('F', 'FEMENINO'),
        ('M', 'MASCULINO')
    )
    cedula = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(default=datetime.date.today)
    sexo = models.CharField(max_length=1, choices=SEXO)
    direccion = models.CharField(max_length=50)
    telefono1 = models.CharField(max_length=50)
    telefono2 = models.CharField(max_length=50)
    fotocopia_cedula = models.ImageField(upload_to='media_root', verbose_name='Imagen')

    def __str__(self):
        return self.nombre
