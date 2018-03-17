from django.urls import path

from .views import list_personas, create_persona, update_persona, delete_persona

urlpatterns = [
    path('', list_personas, name='list_personas'),
    path('new', create_persona, name='create_persona'),
    path('<int:id>/', update_persona, name='update_persona'),
    path('delete/<int:id>', delete_persona, name='delete_persona'),
]

# CRUD - CREATE, READ, UPDATE, DELETE
