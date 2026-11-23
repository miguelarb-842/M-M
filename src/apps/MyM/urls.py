from django.urls import path

from .controllers.home import inicio, perfil
from .controllers.auth import iniciar_sesion, cerrar_sesion
from .controllers.catalogo import catalogo
from .controllers.inventario import inventario, listar_movimientos, detalle_movimiento, registrar_movimiento
from .controllers.ventas import ventas
from .controllers.compras import compras

app_name = 'MyM'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('catalogo/', catalogo, name='catalogo'),
    path('inventario/', inventario, name='inventario'),
    path('inventario/movimientos/', listar_movimientos, name='listar_movimientos'),
    path('inventario/movimiento/<int:movimiento_id>/', detalle_movimiento, name='detalle_movimiento'),
    path('inventario/movimiento/registrar/', registrar_movimiento, name='registrar_movimiento'),
    path('ventas/', ventas, name='ventas'),
    path('compras/', compras, name='compras'),
    path('perfil/', perfil, name='perfil'),
]
