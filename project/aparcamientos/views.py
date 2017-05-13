
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
import urllib
from django.template import loader
# Create your views here.


"""
Página principal del sitio
"""
def Principal(request):
    return(HttpResponse('Principal'))

"""
Página de un usuario determinado
"""
def Profile(request, usuario):
    return(HttpResponse('Perfil de '+ usuario))

"""
Página about del sitio
"""
def About(request):
    return(HttpResponse('About'))

"""
Página con la info de un determinado aparcamiento
"""
def InfoAparcamiento(request, id):
    return(HttpResponse('Info de un aparcamiento '+id))

"""
Página con el XML de un usuario determinado
"""
def UserXML(request, user):
    return(HttpResponse('XML de '+user))

"""
Página de info por si se introduce un recurso no válido
"""
def NoMatch(request):
    return(HttpResponse('El recurso solicitado no se encuentra alojado en el servidor'))
