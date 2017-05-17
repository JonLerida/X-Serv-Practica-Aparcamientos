"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^prueba$', "aparcamientos.views.Prueba", name='Principal'),
    # /
    url(r'^$', "aparcamientos.views.Principal", name='Principal'),
    #página about
    url(r'^about$', "aparcamientos.views.About", name='About'),
    #Login
    url(r'^login/$', "aparcamientos.views.Login", name='Login de un usuario'),
    #logout
    url(r'^logout/$', logout, {'next_page': '/'}),
    #/aparcamientos
    url(r'^aparcamientos$', "aparcamientos.views.InfoAparcamientos", name='InfoAparcamiento'),
    #aparcamiento/id
    url(r'^aparcamientos/([0-9]+)$', "aparcamientos.views.InfoAparcamiento_id", name='InfoAparcamiento'),
    #usuario/xml
    url(r'^([a-zA-Z]+)/xml$', "aparcamientos.views.UserXML", name='UserXML'),
    # Admin site
    url(r'^admin/', include(admin.site.urls)),
    # cadena de letras mayúsculas o minúsculas, no vacía. Es decir, un usuario
    url(r'^([a-zA-Z]+[0-9]*)$', "aparcamientos.views.Profile", name='Profile'),
    # No match
    url(r'^.*$', "aparcamientos.views.NoMatch", name='NoMatch'),
]
