from django.db import models

# Create your models here.


class Usuario (models.Model):
    nick = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    aparcamientos = models.ManyToManyField('Aparcamiento')
    def __str__(self):
        return self.nick

class Aparcamiento (models.Model):
    #number == id, no me deja django llamarlo id creo
    number = models.CharField(max_length = 5)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    accesible = models.CharField(max_length=1)
    latitud = models.CharField(max_length=200)
    longitud = models.CharField(max_length=200)
    barrio = models.CharField(max_length=200)
    distrito = models.CharField(max_length=200)
    datos = models.CharField(max_length=200)

    def __str__(self):
        return (self.number+'  '+self.nombre)

class Comentario (models.Model):
    usuario = models.ForeignKey(Usuario, null = True)
    aparcamiento = models.ForeignKey(Aparcamiento, null=True)
    texto = models.TextField()
    fecha = models.DateTimeField()
    def __str__(self):
        return (self.texto+' '+self.usuario)

class Pagina(models.Model):
    usuario = models.ForeignKey(Usuario)
    nombre = models.CharField(max_length=200)
    enlace = models.CharField(max_length=200, default='')
    def __str__(self):
        return ('Pagina de ' + self.usuario.nick)
