from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import list_alumnos, create_alumno, update_alumno, delete_alumno, list_personas, create_persona, \
    update_persona, delete_persona, list_empleados, update_empleado, create_empleado, delete_empleado, list_profesores, \
    create_profesor, update_profesor, delete_profesor, list_titulares, create_titular, update_titular, delete_titular, \
    list_cuentas, create_cuenta, update_cuenta, delete_cuenta, ProfesorAutocomplete

from main import views

urlpatterns = [
    # Autocomplete
    path('profesor-autocomplete/', ProfesorAutocomplete.as_view(), name='profesor-autocomplete'),

    # Cruds
    path('', views.index),
    path('404', views.error404, name='404'),
    path('accounts/profile/', views.redirect_to_index),
    path('accounts/logout/', LogoutView.as_view(next_page='login', template_name='registration/logged_out.html')),
    path('accounts/', include('django.contrib.auth.urls')),


    path('personas', list_personas, name='list_personas'),
    path('personas/new', create_persona, name='create_persona'),
    path('personas/<int:id>/', update_persona, name='update_persona'),
    path('personas/delete/<int:id>', delete_persona, name='delete_persona'),

    path('alumnos', list_alumnos, name='list_alumnos'),
    path('alumnos/new', create_alumno, name='create_alumno'),
    path('alumnos/<int:id>/', update_alumno, name='update_alumno'),
    path('alumnos/delete/<int:id>', delete_alumno, name='delete_alumno'),

    path('empleados', list_empleados, name='list_empleados'),
    path('empleados/new', create_empleado, name='create_empleado'),
    path('empleados/<int:id>/', update_empleado, name='update_empleado'),
    path('empleados/delete/<int:id>', delete_empleado, name='delete_empleado'),

    path('profesores', list_profesores, name='list_profesores'),
    path('profesores/new', create_profesor, name='create_profesor'),
    path('profesores/<int:id>/', update_profesor, name='update_profesor'),
    path('profesores/delete/<int:id>', delete_profesor, name='delete_profesor'),

    path('titulares', list_titulares, name='list_titulares'),
    path('titulares/new', create_titular, name='create_titular'),
    path('titulares/<int:id>/', update_titular, name='update_titular'),
    path('titulares/delete/<int:id>', delete_titular, name='delete_titular'),

    path('cuentas', list_cuentas, name='list_cuentas'),
    path('cuentas/new', create_cuenta, name='create_cuenta'),
    path('cuentas/<int:id>/', update_cuenta, name='update_cuenta'),
    path('cuentas/delete/<int:id>', delete_cuenta, name='delete_cuenta'),

  

]

