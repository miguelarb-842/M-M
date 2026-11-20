from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render


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
    """
    Propósito:
        Permitir el acceso a las vistas sin autenticación cuando se usa el
        modo demostración, y exigir el inicio de sesión cuando se trabaja
        con la aplicación real.

    Args:
        vista (callable): Función de vista que se quiere proteger.

    Returns:
        callable: La misma vista en modo demostración o la vista envuelta
        por login_required en modo real.
    """
    if settings.DEMO_MODE:
        return vista
    return login_required(vista)


@acceso_requerido
def inicio(request):
    """
    Propósito:
        Mostrar la página principal del sistema y servir como punto de
        entrada a los módulos de la aplicación.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Página de inicio con la lista de módulos disponibles.
    """
    return render(request, 'MyM/inicio.html', {'modulos': MODULOS})


@acceso_requerido
def catalogo(request):
    """
    Propósito:
        Reservar la ruta del catálogo mientras se prepara la interfaz con
        sus datos y operaciones.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Página provisional del módulo de catálogo.
    """
    return render(request, 'MyM/en_construccion.html', {'modulo': 'Catálogo'})


@acceso_requerido
def inventario(request):
    """
    Propósito:
        Reservar la ruta del inventario mientras se prepara la interfaz con
        sus datos y operaciones.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Página provisional del módulo de inventario.
    """
    return render(request, 'MyM/en_construccion.html', {'modulo': 'Inventario'})


@acceso_requerido
def ventas(request):
    """
    Propósito:
        Reservar la ruta de ventas mientras se prepara la interfaz con sus
        datos y operaciones.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Página provisional del módulo de ventas.
    """
    return render(request, 'MyM/en_construccion.html', {'modulo': 'Ventas'})


@acceso_requerido
def compras(request):
    """
    Propósito:
        Reservar la ruta de compras mientras se prepara la interfaz con sus
        datos y operaciones.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Página provisional del módulo de compras.
    """
    return render(request, 'MyM/en_construccion.html', {'modulo': 'Compras'})


@acceso_requerido
def perfil(request):
    """
    Propósito:
        Reservar la ruta del perfil mientras se prepara la información de la
        identidad de demostración o del usuario autenticado.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Página provisional del módulo de perfil.
    """
    return render(request, 'MyM/en_construccion.html', {'modulo': 'Perfil'})


def iniciar_sesion(request):
    """
    Propósito:
        Mostrar el acceso al sistema. En modo demostración presenta una
        identidad visual sin autenticar usuarios reales; en modo real utiliza
        el LoginView nativo de Django.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Página de inicio de sesión o respuesta del LoginView.
    """
    if settings.DEMO_MODE:
        return render(request, 'MyM/login.html')
    return LoginView.as_view(template_name='MyM/login.html')(request)


def cerrar_sesion(request):
    """
    Propósito:
        Cerrar la sesión real del usuario o regresar al inicio cuando se
        trabaja en modo demostración, donde no existe una sesión autenticada.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        HttpResponse: Redirección al inicio o respuesta del LogoutView.
    """
    if settings.DEMO_MODE:
        return redirect('MyM:inicio')
    return LogoutView.as_view(next_page='MyM:login')(request)
