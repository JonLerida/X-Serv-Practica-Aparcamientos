from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Estilo(models.Model):
    usuario = models.ForeignKey(User)
    size = models.IntegerField(default='1')
    color = models.CharField(max_length=20, default='black')
    def __str__(self):
        return 'Estilo' + str(self.id)
class Guardado(models.Model):
    usuario = models.ForeignKey(User)
    aparcamiento = models.ForeignKey('Aparcamiento')
    fecha = models.DateTimeField()
    def __str__(self):
        return str(self.id)

class Usuario (models.Model):
    nick = models.CharField(max_length=200, blank = True)
    password = models.CharField(max_length=200, blank = True)
    aparcamientos = models.ManyToManyField('Aparcamiento')
    def __str__(self):
        return self.nick

class Aparcamiento (models.Model):
    #number == id, no me deja django llamarlo id creo
    number = models.CharField(max_length = 10, default='')
    nombre = models.CharField(max_length=200, default='')
    descripcion = models.TextField(default = '', blank = True)
    accesible = models.BooleanField(default=False)
    url = models.CharField(max_length=200, default='', blank = True)
    via = models.CharField(max_length=100, default='', blank=True)
    localidad = models.CharField(max_length=100, default='', blank=True)
    provincia = models.CharField(max_length=30, default='', blank = True)
    codigo_postal = models.CharField(max_length = 10, default='', blank = True)
    barrio = models.CharField(max_length=200, default='', blank = True)
    distrito = models.CharField(max_length=200, default='', blank = True)
    latitud = models.CharField(max_length=200, default='', blank = True)
    longitud = models.CharField(max_length=200, default='',blank = True)
    datos = models.CharField(max_length=200, default='', blank = True)

    def __str__(self):
        return (self.number+'  '+self.nombre)

class Comentario (models.Model):
    usuario = models.ForeignKey(User, null = True)
    aparcamiento = models.ForeignKey(Aparcamiento, null=True)
    texto = models.TextField()
    fecha = models.DateTimeField()
    def __str__(self):
        return (self.texto)

class Pagina(models.Model):
    usuario = models.ForeignKey(User)
    nombre = models.CharField(max_length=200, default='')
    enlace = models.CharField(max_length=200, default='')
    def __str__(self):
        return ('Pagina de ')
