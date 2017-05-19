
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


KeyItemsSecond = [
            'NOMBRE-VIA', 'CLASE-VIAL', 'LOCALIDAD','PROVINCIA',
            'CODIGO-POSTAL', 'BARRIO', 'DISTRITO', 'LATITUD', 'LONGITUD',
            'TELEFONO', 'EMAIL',
    ]   #campos que voy a guardar
KeyItemsFirst = [
            'ID-ENTIDAD', 'NOMBRE', 'DESCRIPCION', 'ACCESIBILIDAD',
            'CONTENT-URL', 'LOCALIZACION', 'DATOSCONTACTOS',
            'TELEFONO', 'EMAIL',
    ]
"""
Diccionario de conversión de nombre de campo del XML a models
"""
Estandar_to_ModelDict = {
            'ID-ENTIDAD': 'number',
            'NOMBRE': 'nombre',
            'DESCRIPCION' : 'descripcion',
            'ACCESIBILIDAD' : 'accesible',
            'CONTENT-URL' : 'url',
            'NOMBRE-VIA' : 'via',
            'LOCALIDAD' : 'localidad',
            'PROVINCIA' : 'provincia',
            'CODIGO-POSTAL' : 'codigo_postal',
            'BARRIO' : 'barrio',
            'DISTRITO' : 'distrito',
            'LATITUD' : 'latitud',
            'LONGITUD' : 'longitud',
            'TELEFONO' : 'telefono',
            'EMAIL' : 'email',
}




def XMLtoDict(XMLurl):
    file = urllib.request.urlopen(XMLurl)
    data = file.read()
    data = xmltodict.parse(data)
    return data

def parse_deeper(loc_field, park_number):
    #para los elementos que tienen más atributos
    LocDict = {}
    for indexLocal, _ in enumerate(loc_field):
        try:
            campo_localizacion = loc_field[indexLocal]['@nombre']
        except KeyError:
            continue
        if campo_localizacion in KeyItemsSecond:
            LocDict[campo_localizacion] = loc_field[indexLocal]['#text']

    return LocDict


def parse_park(park_item):
    ParkDict = {}   # vacío el diccionario porque si no sobreescribe lo mismo y guarda lo anterior
    for index, item in enumerate(park_item):
        aux_park_dict = {}
        campo = park_item[index]['@nombre']
        if campo == 'LOCALIZACION' or campo == 'DATOSCONTACTOS':    #tengo que profundizar en el árbol
            try:                                                    # puede fallar porque algunos aparcamientos tienen Datos de contacto y otros no... (xd)
                aux_park_dict = parse_deeper(park_item[index]['atributo'], index)
            except KeyError:
                pass
        elif campo in KeyItemsFirst:                # es dato básico
            aux_park_dict = {campo: park_item[index]['#text']}

        ParkDict.update(aux_park_dict)     #d.update(dict2)
    return ParkDict

def Prueba(request):
    ParkList = []
    data = XMLtoDict('http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full')
    aparcamientos = data['Contenidos']['contenido'] #267 aparcamientos
    for  park in aparcamientos:
        ParkList.append(parse_park(park['atributos']['atributo']))
    #Guardamos los aparcamientos
    for Park in ParkList:
        dicc = {}
        model_dict_create = {}
        for property in Park:
            try:
                model_property = Estandar_to_ModelDict[property]
                if property == 'ACCESIBILIDAD':
                    if Park[property] == '1':
                        model_dict_create['accesible'] = True
                    else:
                        model_dict_create['accesible'] = False

                else :
                    model_dict_create[model_property] = Park[property]
            except KeyError:
                continue

        #AparcamientoMod.objects.create(**model_dict_create)

    return HttpResponse('Parseado y guardado')
"""
Devuelve dos objetos: uno con los usuarios que tienen páginas creadas (nombres personalizados)
y otro con los usuarios restantes.
"""
def Get_UserPages_Names(page_object, usuario_object):
    usuarios_con_pagina = page_object.values_list('usuario__username', flat=True)
    list_user = []
    for user in usuarios_con_pagina:
        list_user.append(user)
    user_object = usuario_object.exclude(username__in = list_user)
    return (page_object, user_object)

"""
Devuelve una lista de los 5 aparcamientos más comentados
"""
def Get_MostCommented(com_obj, park_obj):
    comments = com_obj.objects.all().order_by('aparcamiento').distinct()[:5]
    names_list = []
    for comment in comments:
        names_list.append(comment.aparcamiento)
    aparcamiento_object = park_obj.objects.filter(nombre__in = names_list)
    return aparcamiento_object
"""
Página principal del sitio: devuelo el banner, formulario de login o mensaje de bienvenida.
Devuelvo el menu horizontal y vertical y lalista de los 5 aparcamientos con más comentarios
"""
@csrf_exempt
def Principal(request):
    if request.method == 'GET':
        template = loader.get_template('index.html')
        aparcamiento_object = Get_MostCommented(ComentarioMod, AparcamientoMod)
        print(aparcamiento_object)
        #top_aparcamientos = ComentarioMod.objects.all().order_by('-aparcamiento__id').unique()[:5]
        [pagina_object, user_object] = Get_UserPages_Names(PaginaMod.objects.all(), UserMod.objects.all())
        context = {
            'top_aparcamientos': aparcamiento_object,
            'paginas': pagina_object,
            'users': user_object,
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
    if request.method=='GET':
        template = loader.get_template("perfil.html")
        try:
            usuario_object = UserMod.objects.get(username=usuario)
            try:
                guardado_object = GuardadoMod.objects.filter(usuario__username = usuario)[:5] #sus aparcamientos
                estilo_object = EstiloMod.objects.get(usuario__username=usuario)              # su estilo
                context = {
                    'usuario' : usuario_object,
                    'estilo': estilo_object,
                    'guardados': guardado_object,
                }
            except EstiloMod.DoesNotExist:
                context = {
                    'usuario' : usuario_object,
                    'estilo': 'black',
                    'user_size': '80',
                }
            # Aquí tengo que mandar los aparcamientos del usuaruo de 5 en 5
        except UserMod.DoesNotExist:
            context = {
                'DoesNotExist': True,
            }
    else:
        return HttpResponse('HAN HECHO ALGO DISTINTO A GET EN /PROFILE')

    return HttpResponse(template.render(context, request))
""" Método que devuelve el objecto 'Estilo' del usuario solicitante.
Busca en la base, si existe el usuario, lo devuelve. Si no, crea uno nuevo con los parámetros por defecto
"""
def Check_Style(usuario):
    background_color_default = '#D8FFD1'
    size_default = '80' # %
    try:
        estilo_object = EstiloMod.objects.get(usuario__username = usuario)
    except EstiloMod.DoesNotExist:
        user_object = UserMod.objects.get(username=usuario)
        estilo_object = EstiloMod.objects.create(usuario = user_object, color = background_color_default, size=size_default)
    return (estilo_object)



"""
Recurso al que se envía el POST cuando un usuario rellena el formulario de personalización de su página
"""
def Personaliza(request):
    template = loader.get_template("personaliza.html")
    #Comprobar si el usuario tiene creada una página de estilo
    usuario = request.user.username
    user_target = request.POST['user']
    print(user_target)
    try:
        # el formulario ha sido para el nombre
        nombre = request.POST['nombre_pagina']
        try:
            pagina_object = PaginaMod.objects.get(usuario__username = user_target)
            pagina_object.nombre = nombre
            pagina_object.save()
        except:
            user_object = UserMod.objects.get(username=user_target)
            PaginaMod.objects.create(usuario = user_object, nombre = nombre, enlace = 'http://localhost:8080/aparcamientos/'+user_target)
    except KeyError:
        # el formulario ha sido para el estilo
        color = request.POST['color']
        size = request.POST['size']
        estilo_object = Check_Style(user_target)
        estilo_object.color = color
        estilo_object.size = size
        estilo_object.save()

    context = {
        'usuario': usuario,
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
        print(request.POST)
        filter_value = request.POST['filtro_value']
        filter_name = request.POST['filtro_name']
        message = 'Mostrando aparcamientos por: ' + filter_name
        if filter_name =='':
            aparcamiento_object = AparcamientoMod.objects.all()
        else:
            aparcamiento_object = AparcamientoMod.objects.filter(**{filter_name: filter_value})
        context = {
            'aparcamientos': aparcamiento_object,
            'message': message,
        }
    return HttpResponse(template.render(context, request))


"""
Página con la info de un determinado aparcamiento
"""
def InfoAparcamiento_id(request, id):
    template = loader.get_template("aparcamiento_id.html")
    if request.method=='GET':
        try:
            aparcamiento_object = AparcamientoMod.objects.get(number=id)
            comentarios_object = ComentarioMod.objects.filter(aparcamiento__number = id)
            context = {
                'aparcamiento':aparcamiento_object,
                'comentarios': comentarios_object,
            }
        except AparcamientoMod.DoesNotExist:
            context = {
                'DoesNotExist': True,
            }
    elif request.method =='POST':
        texto = request.POST['comentario']
        aparcamiento_object = AparcamientoMod.objects.get(number=id)
        usuario = request.user.username
        usuario_object = UserMod.objects.get(username = usuario)
        ComentarioMod.objects.create(
            usuario = usuario_object,
            texto = texto,
            aparcamiento = aparcamiento_object,
        )
        comentarios_object = ComentarioMod.objects.filter(aparcamiento__number=id)
        context = {
            'aparcamiento':aparcamiento_object,
            'comentarios': comentarios_object,
                    }
        #crear el nuevo comentario
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
