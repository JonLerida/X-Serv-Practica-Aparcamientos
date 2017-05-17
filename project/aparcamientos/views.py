
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login
from django.template import loader
from django.shortcuts import redirect
import xml.sax
from .models import Estilo as EstiloMod
from .models import Usuario as UsuarioMod
from .models import Aparcamiento as AparcamientoMod
from .models import Comentario as ComentarioMod
from .models import Pagina as PaginaMod
from .models import Guardado as GuardadoMod
from django.contrib.auth.models import User as UserMod
# Parseadores
from xml.sax.handler import ContentHandler
import xml.sax
import xml.parsers.expat
import xml.sax
import urllib
import xmltodict


def Prueba(request):
    file = urllib.request.urlopen('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
    data = file.read()
    data = xmltodict.parse(data)
    """
    Listas de los datos parseados del fichero XML:
    De los índices 0-4 de 'atributo'--> datos generales del aparcamiento
    Para el índice 5, hay que volver a indexar la lista--> atributo
    #text--> valor del campo
    @name --> nombre del campo
    """
    id_parsed_list = []
    nombre_parsed_list = []
    descripcion_parsed_list = []
    accesibilidad_parsed_list = []
    url_parsed_list = []
    via_parsed_list = []
    localidad_parsed_list = []
    provincia_parsed_list = []
    codigo_parsed_list = []
    barrio_parsed_list = []
    distrito_parsed_list = []
    latitud_parsed_list = []
    longitud_parsed_list = []

    for indexPark, _ in enumerate(data['Contenidos']['contenido'][0:10], 0):
        # indices del 0-4: datos generales en contenidos-contenido-atributos-atributo
        id_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][0]['#text'])
        nombre_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][1]['#text'])
        descripcion_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][2]['#text'])
        accesibilidad_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][3]['#text'])
        url_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][4]['#text'])
        # indices del 5 en adelante, datos de localizacion
        via_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][0]['#text'])
        localidad_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][4]['#text'])
        provincia_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][5]['#text'])
        codigo_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][6]['#text'])
        barrio_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][7]['#text'])
        distrito_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][8]['#text'])
        latitud_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][-2]['#text'])
        longitud_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][-1]['#text'])



    for index, _ in enumerate(id_parsed_list):
        number = id_parsed_list[index]
        nombre = nombre_parsed_list[index]
        descripcion = descripcion_parsed_list[index]
        accesible = accesibilidad_parsed_list[index]
        url = url_parsed_list[index]
        via = via_parsed_list[index]
        localidad = localidad_parsed_list[index]
        provincia = provincia_parsed_list[index]
        cp = codigo_parsed_list[index]
        barrio = barrio_parsed_list[index]
        distrito = distrito_parsed_list[index]
        latitud = latitud_parsed_list[index]
        longitud = longitud_parsed_list[index]
        #guardamos
        new = AparcamientoMod(
            number= number,
            nombre = nombre,
            descripcion = descripcion,
            accesible=accesible,
            url=url,
            localidad=localidad,
            provincia=provincia,
            codigo_postal = cp,
            barrio = barrio,
            distrito = distrito,
            latitud = latitud,
            longitud = longitud,
        )
        new.save()
    return HttpResponse(data['Contenidos']['contenido'][9]['atributos']['atributo'][5]['atributo'][-1]['#text'])






"""
Página principal del sitio: devuelo el banner, formulario de login o mensaje de bienvenida.
Devuelvo el menu horizontal y vertical y lalista de los 5 aparcamientos con más comentarios
"""
@csrf_exempt
def Principal(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            logged = 'Logged in as '+ request.user.username
        else:
            logged = 'Not logged in.'
        template = loader.get_template('index.html')

        top_aparcamientos = AparcamientoMod.objects.all()[1:6]
        #top_aparcamientos = ComentarioMod.objects.all().order_by('-aparcamiento__id').unique()[:5]
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
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    template = loader.get_template('index.html')
    context = {

    }
    if user is not None:
        login(request, user)
    else:
        # Return an 'invalid login' error message.
        print('fallo')
    return redirect('/') 

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
            guardado_object = GuardadoMod.objects.filter(usuario__nick = usuario)[:5]
            context = {
                'user_nick' : usuario_object.nick,
                'user_color': estilo_object.color,
                'user_size': estilo_object.size,
                'guardados': guardado_object,
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
