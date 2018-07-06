from django.contrib.auth.views import LogoutView
from django.urls import path, include

from main.views import verificar_inscripcion

from .views import list_clases, list_etiquetas, list_etiquetas_clase, \
    list_etiquetas_grupo, list_grupos, list_inscripciones, update_asistencia, update_clase, \
    update_etiqueta, update_etiquetas_clase, update_etiquetas_grupo, update_grupo, update_inscripcion, \
    create_asistencia, create_clase, \
    create_etiqueta, create_etiquetas_clase, create_etiquetas_grupo, create_grupo, create_inscripcion, \
    delete_clase, delete_etiqueta, delete_etiquetas_clase, delete_etiquetas_grupo, \
    delete_grupo, ClaseAutocomplete, GrupoAutocomplete, GrupoAutocompleteAsistencia, \
    lista_asistencia, guardar_inscripcion, list_cuentas, baja_inscripcion, list_inscripciones_baja, \
    list_inscripciones_inactivas, update_cuenta, delete_cuenta, export_alumnos_csv, export_profesores_csv, \
    export_clases_csv, export_grupos_csv, export_titulares_csv, export_empleados_csv

from main import views

urlpatterns = [
    # Autocomplete
    path('clases-autocomplete/', ClaseAutocomplete.as_view(), name='clases-autocomplete'),

    # Cruds
    path('', views.index),
    path('404', views.error404, name='404'),

    path('asistencias', lista_asistencia, name='lista_asistencia'),
    path('asistencia/update', update_asistencia, name='update_asistencia'),
    path('asistencia/new', create_asistencia, name='create_asistencia'),

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
    path('inscripciones/inactivas', list_inscripciones_inactivas, name='list_inscripciones_inactivas'),
    path('inscripciones/bajas', list_inscripciones_baja, name='list_inscripciones_baja'),
    path('inscripciones/new', create_inscripcion, name='create_inscripcion'),
    path('inscripciones/<int:id>/update', update_inscripcion, name='update_inscripcion'),
    # path('inscripciones/<int:id>/delete', delete_inscripcion, name='delete_inscripcion'),
    path('inscripciones/verificar', verificar_inscripcion, name='verificar_inscripcion'),
    path('inscripciones/guardar', guardar_inscripcion, name='guardar_inscripcion'),

    path('inscripciones/<int:id>/baja', baja_inscripcion, name='baja_inscripcion'),


    path('cuentas', list_cuentas, name='list_cuentas'),
    path('cuentas/<int:id>/update', update_cuenta, name='update_cuenta'),
    path('cuentas/<int:id>/delete', delete_cuenta, name='delete_cuenta'),
    # path('ventas/<str:nro_factura>', list_ventas ,name='list_ventas'),


     path('alumnos/csv', export_alumnos_csv, name='export_alumnos_csv'),
     path('profesores/csv', export_profesores_csv, name='export_profesores_csv'),
     path('titulares/csv', export_titulares_csv, name='export_titulares_csv'),
     path('empleados/csv', export_empleados_csv, name='export_empleados_csv'),
     path('clases/csv', export_clases_csv, name='export_clases_csv'),
     path('grupos/csv', export_grupos_csv, name='export_grupos_csv'),



]
