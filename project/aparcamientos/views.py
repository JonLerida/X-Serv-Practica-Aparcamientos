
from django.shortcuts import render
from django.http import HttpResponse
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
Página principal del sitio: devuelo el banner, formulario de login o mensaje de bienvenida.
Devuelvo el menu horizontal y vertical y lalista de los 5 aparcamientos con más comentarios
"""
@csrf_exempt
def Principal(request):
    if request.method == 'GET':
        template = loader.get_template('index.html')
        top_aparcamientos = AparcamientoMod.objects.all()
        pagina_list = PaginaMod.objects.all()
        context = {
            'top_aparcamientos': top_aparcamientos,
            'pagina_list': pagina_list,
            }
    else:
        template = loader.get_template('plana.html')
        context = {
            'title': '405 Method Not Allowed',
        }
    return HttpResponse(template.render(context, request))

"""
Cuando recibo un LOGIN: si el método es POST, compruebo si el nick y password coinciden con la base de datos. Si lo hacen, debería autenticar al usuario, usar
el login ese de las diapos, no se como. Si falla, no lo autentico. En cualquier caso, aunque el método sea invalido, redireccion a la pagina principal
"""
@csrf_exempt
def Login(request):
    template = loader.get_template('login.html')
    if request.method == 'POST':
        nick = request.POST['nick']
        password = request.POST['password']
        try:
            real_user = UsuarioMod.objects.get(nick=nick)
            title2 = 'Usuario si existe'
            if real_user.password == password:
                texto_central = 'OK Volviendo a la página principal...'
            else:
                texto_central = 'KO Volviendo a la página principal...'
        except UsuarioMod.DoesNotExist:
            title2 = 'Usuario No existe'
            texto_central = ''
        context = {
            'title2': title2,
            'login_success': True,
            'text_centeal': texto_central,
            }
    else:
        context = {
            'title2':'Método Invalido',
        }
    return HttpResponse(template.render(context, request))


"""
Página de un usuario determinado: mostrar aparcamientos seleccionados por ese usuario, de 5 en 5
"""
def Profile(request, usuario):
    usuario_object = UsuarioMod.objects.get(nick=usuario)
    return(HttpResponse('Perfil de '+ usuario))

"""
Página about del sitio
"""
def About(request):
    template = loader.get_template("about.html")
    context = {

    }
    return HttpResponse(template.render(context, request))


"""
Página con la info básica de todos los aparcamientos
"""
def InfoAparcamientos(request):
    template = loader.get_template("aparcamientos.html")
    context = {

    }
    return HttpResponse(template.render(context, request))


"""
Página con la info de un determinado aparcamiento
"""
def InfoAparcamiento_id(request, id):
    print(id)
    template = loader.get_template("aparcamiento_id.html")
    context = {
        'aparcamiento_id:': id,
    }
    return HttpResponse(template.render(context, request))

"""
Página con el XML de un usuario determinado
"""
def UserXML(request, user):
    return(HttpResponse('XML de '+user))

"""
Página de info por si se introduce un recurso no válido
"""
def NoMatch(request):
    template = loader.get_template("nomatch.html")
    context = {

    }
    return HttpResponse(template.render(context, request))
