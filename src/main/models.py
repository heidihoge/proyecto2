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
    telefono1 = models.CharField(max_length=50, null=True, blank=True)
    telefono2 = models.CharField(max_length=50, null=True, blank=True)
    fotocopia_cedula = models.ImageField(upload_to='media_root', verbose_name='Fotocopia de Cédula', null=True, blank=True)
    ESTADO = (('A', 'ACTIVO'),
              ('IN', 'INACTIVO'))
    estado = models.CharField(max_length=1, choices=ESTADO, default='A')

    def __str__(self):
        return "{1} {2} ({0})".format(self.cedula, self.nombre, self.apellido)


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

    def __str__(self):
        return "{1} {2} ({0})".format(self.cedula, self.nombre, self.apellido)

#Alumno

class Alumno(Persona):
    imagen = models.ImageField(upload_to='media_root', verbose_name='Foto', null=True, blank=True)
    ficha = models.FileField(upload_to='media_root',  verbose_name='Ficha médica', null=True, blank=True)
    ficha_inscripcion = models.FileField(upload_to='media_root', verbose_name='Ficha de inscripción', null=True, blank=True)
    titular_cuenta = models.ForeignKey(Titular, on_delete=models.SET_NULL,
    blank=True,
    null=True)
    def __str__(self):
        return "{1} {2} ({0})".format(self.cedula, self.nombre, self.apellido)
#Empleado

class Empleado(Persona):
    rol=  models.CharField(max_length=50, default='Profesor', null=True)
    salario = models.IntegerField(default=0)
    def __str__(self):
        return "{1} {2} ({0})".format(self.cedula, self.nombre, self.apellido)

#Profesor
class Profesor(Empleado):
    especialidad = models.CharField(max_length=50)
    def __str__(self):
        return "{1} {2} ({0})".format(self.cedula, self.nombre, self.apellido)


