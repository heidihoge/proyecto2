from django.urls import path

from .views import list_clases, create_clase, update_clase, delete_clase

urlpatterns = [
    path('', list_clases, name='list_clases'),
    path('new', create_clase, name='create_clase'),
    path('<int:id>/', update_clase, name='update_clase'),
    path('delete/<int:id>', delete_clase, name='delete_clase'),
]
