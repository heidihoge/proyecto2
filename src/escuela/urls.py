from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import list_asistencias, list_clases, list_etiquetas, list_etiquetas_clase, \
    list_etiquetas_grupo, list_grupos, list_inscripciones, update_asistencia, update_clase, \
    update_etiqueta, update_etiquetas_clase, update_etiquetas_grupo, update_grupo, update_inscripcion, \
    create_asistencia, create_clase, \
    create_etiqueta, create_etiquetas_clase, create_etiquetas_grupo, create_grupo, create_inscripcion, \
    delete_asistencia, delete_clase, delete_etiqueta, delete_etiquetas_clase, delete_etiquetas_grupo, \
    delete_grupo, delete_inscripcion, ClaseAutocomplete, GrupoAutocomplete, GrupoAutocompleteAsistencia, \
    lista_asistencia

from main import views

urlpatterns = [
    # Autocomplete
    path('clases-autocomplete/', ClaseAutocomplete.as_view(), name='clases-autocomplete'),

    # Cruds
    path('', views.index),
    path('404', views.error404, name='404'),
    path('accounts/profile/', views.redirect_to_index),
    path('accounts/logout/', LogoutView.as_view(next_page='login', template_name='registration/logged_out.html')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('asistencia', list_asistencias, name='list_asistencias'),
    path('asistencias', lista_asistencia, name='lista_asistencia'),
    path('asistencia/new', create_asistencia, name='create_asistencia'),
    path('asistencia/<int:id>/update', update_asistencia, name='update_asistencia'),
    path('asistencia/<int:id>/delete', delete_asistencia, name='delete_asistencia'),

    path('clases', list_clases, name='list_clases'),
    path('clases/new', create_clase, name='create_clase'),
    path('clases/<int:id>/update', update_clase, name='update_clase'),
    path('clases/<int:id>/delete', delete_clase, name='delete_clase'),

    # path('horario', list_dia_horas, name='list_dia_horas'),
    # path('horario/new', create_dia_hora, name='create_dia_hora'),
    # path('horario/<int:id>/update', update_dia_hora, name='update_dia_hora'),
    # path('horario/<int:id>/delete', delete_dia_hora, name='delete_dia_hora'),

    path('etiqueta', list_etiquetas, name='list_etiquetas'),
    path('etiqueta/new', create_etiqueta, name='create_etiqueta'),
    path('etiqueta/<int:id>/update', update_etiqueta, name='update_etiqueta'),
    path('etiqueta/<int:id>/delete', delete_etiqueta, name='delete_etiqueta'),

    path('etiqueta_clase', list_etiquetas_clase, name='list_etiquetas_clase'),
    path('etiqueta_clase/new', create_etiquetas_clase, name='create_etiquetas_clase'),
    path('etiqueta_clase/<int:id>/update', update_etiquetas_clase, name='update_etiquetas_clase'),
    path('etiqueta_clase/<int:id>/delete', delete_etiquetas_clase, name='delete_etiquetas_clase'),

    path('etiqueta_grupo', list_etiquetas_grupo, name='list_etiquetas_grupo'),
    path('etiqueta_grupo/new', create_etiquetas_grupo, name='create_etiquetas_grupo'),
    path('etiqueta_grupo/<int:id>/update', update_etiquetas_grupo, name='update_grupo'),
    path('etiqueta_grupo/<int:id>/delete', delete_etiquetas_grupo, name='delete_etiquetas_grupo'),

    path('grupos', list_grupos, name='list_grupos'),
    path('grupos/new', create_grupo, name='create_grupo'),
    path('grupos/<int:id>/update', update_grupo, name='update_grupo'),
    path('grupos/<int:id>/delete', delete_grupo, name='delete_grupo'),

    path('grupo-autocomplete/', GrupoAutocomplete.as_view(), name='grupo-autocomplete'),
    path('grupo-autocomplete-asistencia/', GrupoAutocompleteAsistencia.as_view(), name='grupo-autocomplete-asistencia'),


    path('inscripciones', list_inscripciones, name='list_inscripciones'),
    path('inscripciones/new', create_inscripcion, name='create_inscripcion'),
    path('inscripciones/<int:id>/update', update_inscripcion, name='update_inscripcion'),
    path('inscripciones/<int:id>/delete', delete_inscripcion, name='delete_inscripcion'),



]
