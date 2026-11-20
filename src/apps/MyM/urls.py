from django.urls import path

from . import views

app_name = 'MyM'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('inventario/', views.inventario, name='inventario'),
    path('ventas/', views.ventas, name='ventas'),
    path('compras/', views.compras, name='compras'),
    path('perfil/', views.perfil, name='perfil'),
]
