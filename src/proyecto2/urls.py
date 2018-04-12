from django.contrib import admin, auth

from django.contrib.auth.views import LogoutView
from django.urls import path, include
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('escuela/', include('escuela.urls')),
    path('compra_venta/', include('tienda.urls')),
    path('404', views.error404, name='404'),
    path('403', views.error403, name='403'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)