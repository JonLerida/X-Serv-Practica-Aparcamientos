
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

"""
Diccionarios para el parser de aparcamientos
"""


KeyItemsLocal = [
            'NOMBRE-VIA', 'CLASE-VIAL', 'NUM', 'LOCALIDAD','PROVINCIA',
            'CODIGO-POSTAL', 'BARRIO', 'DISTRITO', 'LATITUD', 'LONGITUD',
    ]   #campos que voy a guardar
KeyItemsFirst = [
    'ID-ENTIDAD', 'NOMBRE', 'DESCRIPCION', 'ACCESIBILIDAD', 'CONTENT-URL', 'LOCALIZACION', 'DATOSCONTACTOS',
    ]

ParkDict = {}
LocDict = {}
aparcamiento_parseado = {}
ParkList = []                   # hacemos un diccionario de aparcamientos. Cada entrada es un diccionario de items del aparcamiento
def XMLtoDict(XMLurl):
    file = urllib.request.urlopen(XMLurl)
    data = file.read()
    data = xmltodict.parse(data)
    return data

def parse_localization(loc_field, park_number):
    #provincia_parsed_list.append (data['Contenidos']['contenido'][indexPark]['atributos']['atributo'][5]['atributo'][5]['#text'])
    for indexLocal, _ in enumerate(loc_field):
        try:
            campo_localizacion = loc_field[indexLocal]['@nombre']
        except KeyError:
            print('si')
            continue
        if campo_localizacion in KeyItemsLocal:
            LocDict[campo_localizacion] = loc_field[indexLocal]['#text']

    return LocDict


def parse_park(park_item):
    for index, item in enumerate(park_item):
        campo = park_item[index]['@nombre']
        if campo == 'LOCALIZACION' or campo == 'DATOSCONTACTOS':                 #tengo que profundizar en el árbol
            print(campo)
            try:
                aux_park_dict = parse_localization(park_item[index]['atributo'], index)
            except KeyError:
                ParkDict.update(aux_park_dict)
        elif campo in KeyItemsFirst:                # es dato básico
            aux_park_dict = {campo: park_item[index]['#text']}
            ParkDict.update({campo:park_item[index]['#text']})     #update(key, value)

    return ParkDict

def Prueba(request):
    data = XMLtoDict('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
    aparcamientos = data['Contenidos']['contenido'] #267 aparcamientos
    for index, park in enumerate(aparcamientos[0], 0):
        parsed_park = parse_park(aparcamientos[index]['atributos']['atributo'])
        ParkList.append(parsed_park)

    """
    for indexPark, Park in enumerate (ParkList):
        new.AparcamientoMod(
            number=Park(indexPark)['ID-IDENTIDAD'],
            nombre =Park(indexPark)['NOMBRE'],
            descripcion=Park(indexPark)['DESCRIPCION'],
            accesible=Park(indexPark)['ACCESIBILIDAD'],
            url=Park(indexPark)['CONTENT-URL'],
            via=Park(indexPark)['NOMBRE-VIA'],
            localidad=Park(indexPark)['LOCALIDAD'],
            provincia=Park(indexPark)['PROVINCIA'],
            codigo_postal=Park(indexPark)['CODIGO-POSTAL'],
            barrio=Park(indexPark)['BARRIO'],
            distrito=Park(indexPark)['DISTRITO'],
            latitud=Park(indexPark)['LATITUD'],
            longitud=Park(indexPark)['LONGITUD'],
        )
        new.save()
    """

    return HttpResponse(ParkList)



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
