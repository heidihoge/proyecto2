from django.urls import path
from .views import list_profesores, create_profesor, update_profesor, delete_profesor

urlpatterns = [
    path('', list_profesores, name='list_profesores'),
    path('new', create_profesor, name='create_profesor'),
    path('<int:id>/', update_profesor, name='update_profesor'),
    path('delete/<int:id>', delete_profesor, name='delete_profesor'),
]


# CRUD - CREATE, READ, UPDATE, DELETE