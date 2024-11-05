from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    tipo_usuario = models.SmallIntegerField(blank=False)
    nombre_usuario = models.CharField(max_length=50, unique=True, blank=False)
    correo_usuario = models.CharField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=128)

class Fuente(models.Model):
    id_fuente = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000)
    fuente_activa = models.BooleanField(blank=False)
    url = models.URLField(max_length=200)
    def __str__(self):
        return f"{self.titulo} {self.url} {self.fuente_activa}"


class Boletin(models.Model):
    id_boletin = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=100)
    ciudad_tratada = models.CharField(max_length=100)
    tematica = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='pdfs/')
    fuente_boletin = models.ForeignKey(Fuente, on_delete=models.CASCADE, related_name='fuente')