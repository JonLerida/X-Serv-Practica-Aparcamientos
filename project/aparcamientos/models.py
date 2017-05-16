from django.db import models

# Create your models here.

class Estilo(models.Model):
    usuario = models.ForeignKey('Usuario')
    size = models.IntegerField(default='1')
    color = models.CharField(max_length=20, default='black')
    def __str__(self):
        return self.usuario


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
    url = models.CharField(max_length=200, default='')
    descripcion = models.TextField()
    accesible = models.CharField(max_length=1)
    latitud = models.CharField(max_length=200)
    longitud = models.CharField(max_length=200)
    provincia = models.CharField(max_length=30, default='')
    codigo_postal = models.CharField(max_length = 10, default='')
    barrio = models.CharField(max_length=200, default='')
    distrito = models.CharField(max_length=200, default='')
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
    nombre = models.CharField(max_length=200, default='')
    enlace = models.CharField(max_length=200, default='')
    def __str__(self):
        return ('Pagina de ' + self.usuario.nick)
