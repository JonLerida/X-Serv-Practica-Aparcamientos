from django.contrib import admin
from .models import Usuario, Comentario, Aparcamiento, Pagina, Estilo, Guardado
# Register your models here.

class EstiloAdmin(admin.ModelAdmin):
    fieldsets = [
        ('usuario', {'fields': ['usuario']}),
        ('tamaño letra', {'fields': ['size']}),
        ('color', {'fields': ['color']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('usuario', 'size', 'color')

class GuardadoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('usuario', {'fields': ['usuario']}),
        ('aparcamiento', {'fields': ['aparcamiento']}),
        ('fecha', {'fields': ['fecha']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('usuario', 'aparcamiento', 'fecha')

class UsuarioAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Nick', {'fields': ['nick']}),
        ('Contraseña', {'fields': ['password']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('nick', 'password')

class ComentarioAdmin(admin.ModelAdmin):
    fieldsets = [
        ('texto', {'fields': ['texto']}),
        ('fecha', {'fields': ['fecha']}),
        ('usuario', {'fields': ['usuario']}),
        ('Aparcamiento', {'fields': ['aparcamiento']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('texto','usuario', 'fecha', 'aparcamiento')

class AparcamientoAdmin(admin.ModelAdmin):
    fieldsets = [
        ('nombre', {'fields': ['nombre']}),
        ('Number', {'fields': ['number']}),
        ('URL', {'fields': ['url']}),
        ('descripcion', {'fields': ['descripcion']}),
        ('accesible', {'fields': ['accesible']}),
        ('latitud', {'fields': ['latitud']}),
        ('longitud', {'fields': ['longitud']}),
        ('provincia', {'fields': ['provincia']}),
        ('barrio', {'fields': ['barrio']}),
        ('distrito', {'fields': ['distrito']}),
        ('codigo_postal', {'fields': ['codigo_postal']}),
        ('datos', {'fields': ['datos']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('number', 'nombre', 'provincia', 'distrito', 'accesible', 'barrio')


class PaginaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('usuario', {'fields': ['usuario']}),
        ('nombre', {'fields': ['nombre']}),
        ('enlace', {'fields': ['enlace']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('usuario','nombre', 'enlace')

admin.site.register(Guardado, GuardadoAdmin)
admin.site.register(Estilo, EstiloAdmin)
admin.site.register(Pagina, PaginaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Aparcamiento, AparcamientoAdmin)
