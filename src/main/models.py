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
    estado = models.CharField(max_length=2, choices=ESTADO, default='A')

    def edad(self):
        today = datetime.date.today()
        edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        if edad == 0:
            meses = 12 - (self.fecha_nacimiento.month - today.month )
            # 12-9= 3   7 - 9 = -2
            if meses <= 1:
                return str(meses) + " mes"
            return str(meses) + " meses"
        if edad == 1:
            return "1 año"
        return str(edad) + " años"

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

    class Meta:
        permissions = (
            ("titular_list", "Listar titular"),
            ("titular_create", "Crear titular"),
            ("titular_update", "Editar titular"),
            ("titular_delete", "Dar de baja titular "),
        )

#Alumno

class Alumno(Persona):
    imagen = models.ImageField(upload_to='media_root', verbose_name='Foto', null=True, blank=True)
    ficha = models.FileField(upload_to='media_root',  verbose_name='Ficha médica', null=True, blank=True)
    ficha_inscripcion = models.FileField(upload_to='media_root', verbose_name='Ficha de inscripción', null=True, blank=True)
    titular_cuenta = models.ForeignKey(Titular, on_delete=models.SET_NULL,
    blank=True,
    null=True)
    def __str__(self):
        return "{1}, {2} ({0})".format(self.cedula, self.nombre, self.apellido)

    class Meta:
        permissions = (
            ("alumno_list", "Listar alumno"),
            ("alumno_create", "Crear alumno"),
            ("alumno_update", "Editar alumno"),
            ("alumno_delete", "Dar de baja alumno"),
        )


#Empleado

class Empleado(Persona):
    rol=  models.CharField(max_length=50, default='Profesor', null=True)
    salario = models.IntegerField(default=0)
    def __str__(self):
        return "{1} {2} ({0})".format(self.cedula, self.nombre, self.apellido)

    class Meta:
        permissions = (
            ("empleado_delete", "Dar de baja empleado"),
            ("empleado_create", "Crear empleado"),
            ("empleado_update", "Editar empleado"),
        )

#Profesor
class Profesor(Empleado):
    especialidad = models.CharField(max_length=50)
    def __str__(self):
        return "{1} {2} ({0})".format(self.cedula, self.nombre, self.apellido)

    class Meta:
        permissions = (
            ("profesor_delete", "Dar de baja empleado"),
            ("profesor_create", "Crear profesor"),
            ("profesor_update", "Editar profesor"),
        )
