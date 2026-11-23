from django.urls import path

from .controllers.home import inicio, perfil
from .controllers.auth import iniciar_sesion, cerrar_sesion
from .controllers.catalogo import catalogo
from .controllers.inventario import inventario
from .controllers.ventas import ventas
from .controllers.compras import compras

app_name = 'MyM'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('catalogo/', catalogo, name='catalogo'),
    path('inventario/', inventario, name='inventario'),
    path('ventas/', ventas, name='ventas'),
    path('compras/', compras, name='compras'),
    path('perfil/', perfil, name='perfil'),
]
