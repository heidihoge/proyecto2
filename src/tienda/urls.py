from django.contrib.auth.views import LogoutView

from django.urls import path, include

from tienda import views
from main import views
from tienda.views import list_productos, create_producto, update_producto, delete_producto, list_categoria_productos, \
    create_categoria_producto, update_categoria_producto, delete_categoria_producto, comprar, list_compras, vender, \
    export_productos_csv, ClienteAutocomplete, FacturaAutocomplete, ProductoAutocomplete, list_clientes, create_cliente, \
    delete_cliente, update_cliente
from tienda.views import list_facturas,create_factura, delete_factura, update_factura, update_compra

urlpatterns = [

    # Cruds
    path('', views.index),
    path('404', views.error404, name='404'),
    path('403', views.error403, name='403'),

    path('cliente-autocomplete/', ClienteAutocomplete.as_view(), name='cliente-autocomplete'),
    path('factura-autocomplete/', FacturaAutocomplete.as_view(), name='factura-autocomplete'),
    path('producto-autocomplete/', ProductoAutocomplete.as_view(), name='producto-autocomplete'),


    path('accounts/profile/', views.redirect_to_index),
    path('accounts/logout/', LogoutView.as_view(next_page='login', template_name='registration/logged_out.html')),
    path('accounts/', include('django.contrib.auth.urls')),


    path('productos', list_productos, name='list_productos'),
    path('productos/new', create_producto, name='create_producto'),
    path('productos/<str:codigo>/update', update_producto, name='update_producto'),
    path('productos/<str:codigo>/delete', delete_producto, name='delete_producto'),

    path('categoria_productos', list_categoria_productos, name='list_categoria_productos'),
    path('categoria_productos/new', create_categoria_producto, name='create_categoria_producto'),
    path('categoria_productos/<int:id>/update', update_categoria_producto, name='update_categoria_producto'),
    path('categoria_productos/<int:id>/delete', delete_categoria_producto, name='delete_categoria_producto'),


    path('facturas', list_facturas, name='list_facturas'),
    path('facturas/new', create_factura, name='create_factura'),
    path('facturas/<int:id>/update', update_factura, name='update_factura'),
    path('facturas/<int:id>/delete', delete_factura, name='delete_factura'),


    path('clientes', list_clientes, name='list_clientes'),
    path('clientes/new', create_cliente, name='create_cliente'),
    path('clientes/<str:ruc_cliente>/update', update_cliente, name='update_cliente'),
    path('clientes/<str:ruc_cliente>/delete', delete_cliente, name='delete_cliente'),

    path('ventas/new', vender, name='vender'),

    path('compras', list_compras, name='list_compras'),
    path('compras/new', comprar, name='comprar'),
    path('compras/<int:id>/update', update_compra, name='update_compra'),

    path('export/csv', export_productos_csv, name='export_productos_csv'),


]


