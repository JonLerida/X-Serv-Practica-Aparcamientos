from django.contrib import admin
from .models import Usuario, Comentario, Aparcamiento, Pagina, Estilo
# Register your models here.

class EstiloAdmin(admin.ModelAdmin):
    fieldsets = [
        ('usuario', {'fields': ['usuario']}),
        ('tamaño letra', {'fields': ['size']}),
        ('color', {'fields': ['coor']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('usuario', 'size', 'color')


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
        ('descripcion', {'fields': ['descripcion']}),
        ('accesible', {'fields': ['accesible']}),
        ('latitud', {'fields': ['latitud']}),
        ('longitud', {'fields': ['longitud']}),
        ('barrio', {'fields': ['barrio']}),
        ('distrito', {'fields': ['distrito']}),
        ('datos', {'fields': ['datos']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('nombre', 'number', 'accesible', 'barrio')


class PaginaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('usuario', {'fields': ['usuario']}),
        ('nombre', {'fields': ['nombre']}),
        ('enlace', {'fields': ['enlace']}),
        #'classes': ['collapse']}),
    ]
    list_display = ('usuario','nombre', 'enlace')

admin.site.register(Estilo, EstiloAdmin)
admin.site.register(Pagina, PaginaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Aparcamiento, AparcamientoAdmin)
