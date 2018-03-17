from django.contrib import admin, auth
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('main.urls')),
    #path('personas/', include('personas.urls')),
    path('alumnos/', include('alumnos.urls')),
    path('profesores/', include('profesores.urls')),
    path('clases/', include('clases.urls'))
    #path('grupos/', include('grupos.urls')),
    #path('diashoras/', include('diashoras.urls')),
    #path('etiquetas/', include('etiquetas.urls'))
    #path('etiquetasclases/', include('etiquetasclases.urls')),
    #path('etiquetasgrupos/', include('etiquetasgrupos.urls')),
    #path('inscripciones/', include('inscripciones.urls')),
    #path('asistencias/', include('asistencias.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
