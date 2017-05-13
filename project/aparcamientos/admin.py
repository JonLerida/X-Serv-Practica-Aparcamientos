from django.contrib import admin
from .models import Usuario, Comentario, Aparcamiento
# Register your models here.
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


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Aparcamiento, AparcamientoAdmin)
