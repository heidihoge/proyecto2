from django.urls import path
from .views import list_alumnos, create_alumno, update_alumno, delete_alumno

urlpatterns = [
    path('', list_alumnos, name='list_alumnos'),
    path('new', create_alumno, name='create_alumno'),
    path('<int:id>/', update_alumno, name='update_alumno'),
    path('delete/<int:id>', delete_alumno, name='delete_alumno'),
]


# CRUD - CREATE, READ, UPDATE, DELETE