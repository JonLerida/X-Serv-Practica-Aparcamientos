
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
import urllib
from django.template import loader
from .models import Estilo as EstiloMod
from .models import Usuario as UsuarioMod
from .models import Aparcamiento as AparcamientoMod
from .models import Comentario as ComentarioMod
from .models import Pagina as PaginaMod
# Create your views here.


"""
Página principal del sitio
"""
@csrf_exempt
def Principal(request):
    template = loader.get_template('index.html')
    top_aparcamientos = AparcamientoMod.objects.all()
    context = {
        'top_aparcamientos': top_aparcamientos,
        }
    return HttpResponse(template.render(context, request))

"""
Cuando recibo un LOGIN
"""
@csrf_exempt
def Login(request):
    template = loader.get_template('login.html')
    if request.method == 'POST':
        respuesta = 'Es post'
    else:
        context = {

        }

    return HttpResponse(respuesta)




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
Página con la info básica de todos los aparcamientos
"""
def InfoAparcamientos(request):
    return(HttpResponse('Info de todos los aparcamientos'))


"""
Página con la info de un determinado aparcamiento
"""
def InfoAparcamiento_id(request, id):
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
