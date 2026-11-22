from django.shortcuts import render

from .home import acceso_requerido


@acceso_requerido
def inventario(request):
    return render(request, 'pages/en_construccion.html', {'modulo': 'Inventario'})
