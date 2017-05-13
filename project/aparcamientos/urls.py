from django.conf.urls import url

from . import views

urlpatterns = [
    # /aparcamientos
    url(r'^$', views.Principal, name='Principal'),
    # cadena de letras mayúsculas o minúsculas, no vacía. Es decir, un usuario
    url(r'^([a-zA-Z]+)$', views.Profile, name='Profile'),
    #página about
    url(r'^about$', views.About, name='About'),
    #aparcamiento/id
    url(r'^([0-9]+)$', views.InfoAparcamiento, name='InfoAparcamiento'),
    #usuario/xml
    url(r'^([a-zA-Z]+)/xml$', views.UserXML, name='UserXML'),
    # No match
    url(r'^.*$', views.NoMatch, name='NoMatch'),
]
