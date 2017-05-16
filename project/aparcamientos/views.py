
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
        top_aparcamientos = ComentarioMod.objects.all().order_by('-aparcamiento__id').unique()[:5]
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
Comprobar si el usuario existe. Si existe, comprobar si tiene un estilo asociado. Si lo tiene, devolverle el estilo. Si no, le ponemos el
estandar (negro,1em)
"""
def Profile(request, usuario):
    template = loader.get_template("perfil.html")
    try:
        usuario_object = UsuarioMod.objects.get(nick=usuario)
        try:
            estilo_object = EstiloMod.objects.get(usuario__nick=usuario)
            context = {
                'user_nick' : usuario_object.nick,
                'user_color': estilo_object.color,
                'user_size': estilo_object.size,
            }
        except EstiloMod.DoesNotExist:
            context = {
                'user_nick' : usuario_object.nick,
                'user_color': 'black',
                'user_size': '1',
            }
        # Aquí tengo que mandar los aparcamientos del usuaruo de 5 en 5
    except UsuarioMod.DoesNotExist:
        context = {
            'DoesNotExist': True,
        }

    return HttpResponse(template.render(context, request))

"""
Página about del sitio
"""
def About(request):
    template = loader.get_template("about.html")
    context = {

    }
    return HttpResponse(template.render(context, request))


"""
Página con la info básica de todos los aparcamientos. Si el método es GET, devuelvo todos los aparcamientos. Si es POST, filtro el distrito
"""
def InfoAparcamientos(request):
    template = loader.get_template("aparcamientos.html")
    if request.method == 'GET':
        aparcamiento_object = AparcamientoMod.objects.all()
        context = {
            'aparcamientos': aparcamiento_object,
        }
    elif request.method == 'POST':
        distrito = request.POST['distrito']
        if distrito =='':
            aparcamiento_object = AparcamientoMod.objects.all()
        else:
            aparcamiento_object = AparcamientoMod.objects.filter(distrito=distrito)
        context = {
            'aparcamientos': aparcamiento_object,
        }
    return HttpResponse(template.render(context, request))


"""
Página con la info de un determinado aparcamiento
"""
def InfoAparcamiento_id(request, id):
    print(id)
    template = loader.get_template("aparcamiento_id.html")
    try:
        aparcamiento_object = AparcamientoMod.objects.get(number=id)
        comentarios_object = ComentarioMod.objects.filter(aparcamiento__number = id)
        context = {
            'aparcamiento_id': id,
            'aparcamiento':aparcamiento_object,
            'comentarios': comentarios_object,
        }
    except AparcamientoMod.DoesNotExist:
        context = {
            'DoesNotExist': True,
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
