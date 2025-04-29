from django.db import models

# Create your models here.

#from django.contrib.postgres.fields import ArrayField  # si usás PostgreSQL

class Grafo(models.Model):
    nombre = models.CharField(max_length=100)
    size = models.IntegerField(default=10)
    inicio = models.JSONField()
    fin = models.JSONField()
    muros = models.JSONField()  # Lista de coordenadas [[x1, y1], [x2, y2], ...]

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre