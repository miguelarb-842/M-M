from django.shortcuts import render

from .home import acceso_requerido


@acceso_requerido
def compras(request):
    return render(request, 'pages/en_construccion.html', {'modulo': 'Compras'})
