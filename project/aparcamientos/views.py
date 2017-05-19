
from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.template import loader
from django.shortcuts import redirect
# Modelos
from .models import Estilo as EstiloMod
from .models import Aparcamiento as AparcamientoMod
from .models import Comentario as ComentarioMod
from .models import Pagina as PaginaMod
from .models import Guardado as GuardadoMod
from django.contrib.auth.models import User as UserMod
from django.db.models import Count
# Parseadores
from xml.sax.handler import ContentHandler
import xml.sax
import xml.parsers.expat
import urllib
import xmltodict

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MÉTODOS Y VARIABLES AUXILIARES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""
Variables para el parser de aparcamientos
"""
XML_URL = 'http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full'

"""
Diccionario de propiedades secundarias de los aparcamientos
"""
KeyItemsSecond = [
            'NOMBRE-VIA', 'CLASE-VIAL', 'LOCALIDAD','PROVINCIA',
            'CODIGO-POSTAL', 'BARRIO', 'DISTRITO', 'LATITUD', 'LONGITUD',
            'TELEFONO', 'EMAIL',
    ]
"""
Diccionario de campos y propiedades primarias de los aparcamientos (las que no son 'profundas')
"""
KeyItemsFirst = [
            'ID-ENTIDAD', 'NOMBRE', 'DESCRIPCION', 'ACCESIBILIDAD',
            'CONTENT-URL', 'LOCALIZACION', 'DATOSCONTACTOS',
            'TELEFONO', 'EMAIL',
    ]
"""
Diccionario de conversión de nombre de campo del XML a models (como lo llama el XML--> como lo llamo yo en Models)
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


"""
Método que devuelve el objecto 'Estilo' del usuario solicitante.
Busca en la base, si existe el usuario, lo devuelve. Si no, crea uno nuevo con los parámetros por defecto
"""
def Check_Style(usuario):
    background_color_default = '#D8FFD1'
    size_default = '80' # en porcentaje
    try:
        estilo_object = EstiloMod.objects.get(usuario__username = usuario)
    except EstiloMod.DoesNotExist:
        user_object = UserMod.objects.get(username=usuario)
        estilo_object = EstiloMod.objects.create(usuario = user_object, color = background_color_default, size=size_default)
    return (estilo_object)

"""
Método que convierte una URL de un XML en un diccionario parseable
"""

def XMLtoDict(XMLurl):
    file = urllib.request.urlopen(XMLurl)
    data = file.read()
    data = xmltodict.parse(data)
    return data
"""
Método para aquellos nodos del árbol XML que tuvieran mayor profundidad
"""
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

"""
Método que parsea un aparcamiento (nodo del árbol XML). Devuelve un diccionario {propiedad: valor}
"""
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
"""
Método que parsea un XML. Devuelve una lista de diccionarios. Cada índice es un aparcamiento
"""
def ParseXML():
    ParkList = []       #Lista de diccionarios. Cada índice de la lista es un aparcamiento y contiene su descripción
    data = XMLtoDict(XML_URL)
    aparcamientos = data['Contenidos']['contenido'] #267 aparcamientos
    for  park in aparcamientos:
        ParkList.append(parse_park(park['atributos']['atributo']))

    return ParkList
"""
Dado un parsed, actualiza la base de datos de aparcamientos
"""
def UpdateDataBase(parsed_list):
    print(parsed_list)
    #Guardamos los aparcamientos
    for Park in parsed_list:
        dicc = {}
        print("Updating 'Aparcamiento' data base...")
        model_dict_create = {}   # diccionario de propiedad: valor, con el nombre dado en el Modelo Django (aparcamiento)
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
                pass
        try:
            #Comprobación para no crear 20 veces el mismo aparcamiento. Si por alguna razón ya existe, pasamos sin más
            AparcamientoMod.objects.get(number = model_dict_create['number'])
            continue
        except AparcamientoMod.DoesNotExist:
            AparcamientoMod.objects.create(**model_dict_create)
            pass

    return None
"""
Devuelve dos objetos: uno con los usuarios que tienen páginas creadas (nombres personalizados)
y otro con los usuarios restantes, de esta forma a cada usuario le damos el nombre de página
adecuado.
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
    # Dame todos los aparcamientos. Dame el contador de comentarios de cada uno. Ordenalos por numero de comentarios. Excluye los que no tengan comentarios.
    aparcamiento_object = AparcamientoMod.objects.annotate(num_coment = Count('comentario')).order_by('-num_coment').exclude(num_coment = 0)[:5]

    return aparcamiento_object


def CheckDataBase():
    if AparcamientoMod.objects.all().count() == 0:
        XML_Parsed = ParseXML()
        UpdateDataBase(XML_Parsed)
        print('actualizada')
    return None


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MÉTODOS DE VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
Página principal del sitio: devuelo el banner, formulario de login o mensaje de bienvenida.
Devuelvo el menu horizontal y vertical y lalista de los 5 aparcamientos con más comentarios
"""
@csrf_exempt
def Principal(request):
    if request.method == 'GET':
        template = loader.get_template('index.html')
        aparcamiento_object = Get_MostCommented(ComentarioMod, AparcamientoMod)
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
            guardado_object = GuardadoMod.objects.filter(usuario__username = usuario)[:5] #sus aparcamientos
            estilo_object = Check_Style(usuario)            # su estilo
            context = {
                'usuario' : usuario_object,
                'estilo': estilo_object,
                'guardados': guardado_object,
            }
        except UserMod.DoesNotExist:
            context = {
                'DoesNotExist': True,
            }
    else:
        return HttpResponse('HAN HECHO ALGO DISTINTO A GET EN /PROFILE')

    return HttpResponse(template.render(context, request))



"""
Recurso al que se envía el POST cuando un usuario rellena el formulario de personalización de su página
"""
def Personaliza(request):
    template = loader.get_template("personaliza.html")
    #Comprobar si el usuario tiene creada una página de estilo
    usuario = request.user.username
    user_target = request.POST['user']
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
        print(color)
        size = request.POST['size']
        estilo_object = Check_Style(user_target)
        estilo_object.color = color
        estilo_object.size = size
        estilo_object.save()

    context = {
        'usuario': user_target,
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
    CheckDataBase()
    template = loader.get_template("aparcamientos.html")
    if request.method == 'GET':
        aparcamiento_object = AparcamientoMod.objects.all()
        context = {
            'aparcamientos': aparcamiento_object,
        }
    elif request.method == 'POST':
        filter_value = request.POST['filtro_value']
        filter_name = request.POST['filtro_name']
        if filter_name =='':
            message = 'No hay filtro seleccionado'
            aparcamiento_object = AparcamientoMod.objects.all()
        else:
            if filter_value == '':
                message = 'Mostrando todos los aparcamientos'
                aparcamiento_object = AparcamientoMod.objects.all()
            else:
                if filter_value =='False' and filter_name == 'accesible':
                    #intercambio por cadena vacía, para que sea False. El string vacío es false
                    filter_value =''
                message = 'Mostrando aparcamientos por: ' + filter_name
                aparcamiento_object = AparcamientoMod.objects.filter(**{filter_name: filter_value})
        count = aparcamiento_object.count()
        context = {
            'aparcamientos': aparcamiento_object,
            'message': message,
            'count': '('+str(count)+')',
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

@csrf_exempt
def add_park(request):
    template = loader.get_template("add_park.html")
    usuario = request.user.username
    park_number = request.POST['park_number']
    try:
        # aparcamientos del usuario
        guardados_user_object = GuardadoMod.objects.filter(usuario__username = usuario)
        try:
            # Comprobar si ya lo tiene guardado
            guardado_object = guardados_user_object.get(aparcamiento__number = park_number)
            #si ya existe, significa que ya lo tenía guardado. No hacemos nada
            message = 'El aparcamiento seleccionado ya pertenece a tu lista!'
            context = {
                'title': message,
                }
            return HttpResponse(template.render(context, request))
        except GuardadoMod.DoesNotExist:
            pass
    except GuardadoMod.DoesNotExist:
        pass
    # no tiene ninguno guardado.
    # Si no existe, lo creamos
    usuario_object = UserMod.objects.get(username = usuario)
    aparcamiento_object = AparcamientoMod.objects.get(number=park_number)
    GuardadoMod.objects.create(
        usuario = usuario_object,
        aparcamiento = aparcamiento_object,
    )
    message = 'Tu lista ha sido actualizada: has añadido el nº'+park_number
    context = {
        'title': message,
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
