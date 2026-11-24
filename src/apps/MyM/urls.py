from django.urls import path

from .controllers.home import inicio, perfil
from .controllers.auth import iniciar_sesion, cerrar_sesion
from .controllers.catalogo import catalogo, detalle_producto
from .controllers.inventario import inventario, listar_movimientos, detalle_movimiento, registrar_movimiento
from .controllers.ventas import ventas
from .controllers.compras import compras
from .controllers.marca import registrar_marca
from .controllers.categoria import registrar_categoria
from .controllers.producto import registrar_producto, editar_producto

app_name = 'MyM'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('catalogo/', catalogo, name='catalogo'),
    path('catalogo/marca/registrar/', registrar_marca, name='registrar_marca'),
    path('catalogo/categoria/registrar/', registrar_categoria, name='registrar_categoria'),
    path('catalogo/producto/registrar/', registrar_producto, name='registrar_producto'),
    path('catalogo/producto/<int:pk>/', detalle_producto, name='detalle_producto'),
    path('catalogo/producto/<int:pk>/editar/', editar_producto, name='editar_producto'),
    path('inventario/', inventario, name='inventario'),
    path('inventario/movimientos/', listar_movimientos, name='listar_movimientos'),
    path('inventario/movimiento/<int:movimiento_id>/', detalle_movimiento, name='detalle_movimiento'),
    path('inventario/movimiento/registrar/', registrar_movimiento, name='registrar_movimiento'),
    path('ventas/', ventas, name='ventas'),
    path('compras/', compras, name='compras'),
    path('perfil/', perfil, name='perfil'),
]
