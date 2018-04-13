from django.contrib.auth.views import LogoutView

from django.urls import path, include

from tienda import views
from main import views
from tienda.views import list_productos, create_producto, update_producto, delete_producto, list_categoria_productos, create_categoria_producto, update_categoria_producto, delete_categoria_producto
from tienda.views import list_facturas,create_factura, delete_factura, update_factura

urlpatterns = [

    # Cruds
    path('', views.index),
    path('404', views.error404, name='404'),
    path('403', views.error403, name='403'),

    path('accounts/profile/', views.redirect_to_index),
    path('accounts/logout/', LogoutView.as_view(next_page='login', template_name='registration/logged_out.html')),
    path('accounts/', include('django.contrib.auth.urls')),


    path('productos', list_productos, name='list_productos'),
    path('productos/new', create_producto, name='create_producto'),
    path('productos/<int:id>/update', update_producto, name='update_producto'),
    path('productos/<int:id>/delete', delete_producto, name='delete_producto'),

    path('categoria_productos', list_categoria_productos, name='list_categoria_productos'),
    path('categoria_productos/new', create_categoria_producto, name='create_categoria_producto'),
    path('categoria_productos/<int:id>/update', update_categoria_producto, name='update_categoria_producto'),
    path('categoria_productos/<int:id>/delete', delete_categoria_producto, name='delete_categoria_producto'),


    path('facturas', list_facturas, name='list_facturas'),
    path('facturas/new', create_factura, name='create_factura'),
    path('facturas/<int:id>/update', update_factura, name='update_factura'),
    path('facturas/<int:id>/delete', delete_factura, name='delete_factura'),

     ]


