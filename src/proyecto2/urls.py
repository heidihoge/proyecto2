from django.contrib import admin, auth
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('main.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)