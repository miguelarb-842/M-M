from django.contrib.auth.decorators import login_required
from django.shortcuts import render


MODULOS = [
    {
        'nombre': 'Catálogo',
        'descripcion': 'Productos, marcas, categorías y variantes.',
        'url': 'MyM:catalogo',
    },
    {
        'nombre': 'Inventario',
        'descripcion': 'Existencias, alertas de stock bajo y movimientos.',
        'url': 'MyM:inventario',
    },
    {
        'nombre': 'Ventas',
        'descripcion': 'Historial, detalle y representación visual de ventas.',
        'url': 'MyM:ventas',
    },
    {
        'nombre': 'Compras',
        'descripcion': 'Historial y detalle de compras a distribuidores.',
        'url': 'MyM:compras',
    },
    {
        'nombre': 'Perfil',
        'descripcion': 'Información del usuario o identidad de demostración.',
        'url': 'MyM:perfil',
    },
]


def acceso_requerido(vista):
    return login_required(vista)


@acceso_requerido
def inicio(request):
    return render(request, 'pages/inicio.html', {'modulos': MODULOS})


@acceso_requerido
def perfil(request):
    return render(request, 'pages/en_construccion.html', {'modulo': 'Perfil'})
