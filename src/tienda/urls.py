from django.contrib.auth.views import LogoutView

from django.urls import path, include

from tienda import views
from main import views
from tienda.views import list_productos, create_producto, update_producto, delete_producto, \
    comprar, list_compras, vender, \
    export_productos_csv, ClienteAutocomplete, FacturaAutocomplete, ProductoAutocomplete, list_clientes, create_cliente, \
    delete_cliente, update_cliente, CuentaAutocomplete, list_ventas, consulta_factura, cancela_venta, list_operaciones, \
    create_operacion, update_operacion, delete_operacion, reporte_compras, list_ventas_canceladas, estado_cuenta, \
    list_ventas_fechas, export_clientes_csv, list_ventas_credito_fechas, list_recibos_fechas, \
    list_ventas_credito_vencimiento_fechas, list_compras_fechas
from tienda.views import list_facturas,create_factura, delete_factura, update_factura, update_compra

urlpatterns = [

    # Cruds
    path('', views.index),
    path('404', views.error404, name='404'),
    path('403', views.error403, name='403'),

    path('cliente-autocomplete/', ClienteAutocomplete.as_view(), name='cliente-autocomplete'),
    path('factura-autocomplete/', FacturaAutocomplete.as_view(), name='factura-autocomplete'),
    path('producto-autocomplete/', ProductoAutocomplete.as_view(), name='producto-autocomplete'),
    path('cuenta-autocomplete/', CuentaAutocomplete.as_view(), name='cuenta-autocomplete'),


    path('productos', list_productos, name='list_productos'),
    path('productos/new', create_producto, name='create_producto'),
    path('productos/<str:codigo>/update', update_producto, name='update_producto'),
    path('productos/<str:codigo>/delete', delete_producto, name='delete_producto'),

    path('facturas', list_facturas, name='list_facturas'),
    path('facturas/new', create_factura, name='create_factura'),
    path('facturas/<int:id>/update', update_factura, name='update_factura'),
    path('facturas/<int:id>/delete', delete_factura, name='delete_factura'),


    path('clientes', list_clientes, name='list_clientes'),
    path('clientes/new', create_cliente, name='create_cliente'),
    path('clientes/<str:ruc_cliente>/update', update_cliente, name='update_cliente'),
    path('clientes/<str:ruc_cliente>/delete', delete_cliente, name='delete_cliente'),

    path('ventas/new', vender, name='vender'),
    path('ventas', list_ventas, name='list_ventas'),
    path('ventas/fechas', list_ventas_fechas, name='list_ventas_fechas'),

    path('recibos/fechas', list_recibos_fechas, name='list_recibo_fechas'),
    path('ventas/credito/fechas', list_ventas_credito_fechas, name='list_ventas_credito_fechas'),
    path('ventas/credito/vencimiento/fechas', list_ventas_credito_vencimiento_fechas, name='list_ventas_credito_vencimiento_fechas'),
    path('ventas/canceladas', list_ventas_canceladas, name='list_ventas_canceladas'),
    path('ventas/<str:nro_factura>', consulta_factura, name='consulta_factura'),

    path('ventas/<int:id>/cancelar', cancela_venta, name='cancela_venta'),

    path('caja', list_operaciones, name='list_operaciones'),
    path('caja/new', create_operacion, name='create_operacion'),
    path('caja/<int:id>/update', update_operacion, name='update_operacion'),
    path('caja/<int:id>/delete', delete_operacion, name='delete_operacion'),

    path('compras/reporte', reporte_compras, name='reporte_compras'),
    path('compras', list_compras, name='list_compras'),
    path('compras/fechas', list_compras_fechas, name='list_compras_fechas'),
    path('compras/new', comprar, name='comprar'),
    path('compras/<int:id>/update', update_compra, name='update_compra'),
    path('productos/csv', export_productos_csv, name='export_productos_csv'),
    path('clientes/csv', export_clientes_csv, name='export_clientes_csv'),

    path('estado_cuenta', estado_cuenta, name='estado_cuenta'),


]


