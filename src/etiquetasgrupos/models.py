from django.db import models

from etiquetas.models import Etiqueta
from grupos.models import Grupo


# Create your models here.

class EtiquetaGrupo(models.Model):
    id_grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    def __str__(self):
        return self.etiqueta
