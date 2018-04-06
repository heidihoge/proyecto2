from django.contrib.auth.views import LogoutView

from django.urls import path, include
# from .views import list_documentos, create_documento, delete_documento, update_documento
from tienda import views
from main import views

urlpatterns = [
    # # Autocomplete
    # path('clases-autocomplete/', ClaseAutocomplete.as_view(), name='clases-autocomplete'),

    # Cruds
    path('', views.index),
    path('404', views.error404, name='404'),
    path('accounts/profile/', views.redirect_to_index),
    path('accounts/logout/', LogoutView.as_view(next_page='login', template_name='registration/logged_out.html')),
    path('accounts/', include('django.contrib.auth.urls')),
     ]