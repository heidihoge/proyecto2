from django.db import models

from clases.models import Clase
from etiquetas.models import Etiqueta


# Create your models here.

class EtiquetaClase(models.Model):
    id_clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    def __str__(self):
        return self.etiqueta
