import datetime
from django.db import models


#persona
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
        return self.nombre + " " + self.apellido


#Titular
class Titular(Persona):
    OPCIONES_TIPO_TUTOR = (
        ('M', 'Madre'),
        ('P', 'Padre'),
        ('H', 'Hermano/a'),
        ('T', 'Tio/a'),
        ('A', 'Abuelo/a'),
        ('E', 'Encargado/a'),
        ('U', 'Unico'),
    )
    tipo_responsable = models.CharField(max_length=1, choices = OPCIONES_TIPO_TUTOR)

#Alumno

class Alumno(Persona):
    imagen = models.ImageField(upload_to='media_root', verbose_name='Imagen')
    ficha= models.FileField(upload_to='media_root')
    ficha_inscripcion = models.FileField(upload_to='media_root')
    titular_cuenta = models.ForeignKey(Titular, on_delete=models.SET_NULL,
    blank=True,
    null=True)
    def __str__(self):
        return self.cedula + " " + self.nombre
#Empleado

class Empleado(Persona):
    salario = models.IntegerField(default=0)
    def __str__(self):
        return self.cedula + " " + self.nombre

#Profesor
class Profesor(Empleado):
    especialidad = models.CharField(max_length=50)

#Cuenta
class Cuenta(models.Model):
    descripcion = models.CharField(max_length=50)
    monto = models.IntegerField()
    saldo = models.IntegerField()
    id_persona = models.ForeignKey(Persona, on_delete=models.SET_NULL,null=True)
