from django.conf import settings


def demo_mode(request):
    """
    Propósito:
        Poner a disposición de todas las plantillas el estado del modo
        demostración y el nombre de la identidad visual utilizada.

    Args:
        request (HttpRequest): Solicitud HTTP realizada por el usuario.

    Returns:
        dict: Diccionario con las variables modo_demo y usuario_demo.
    """
    return {
        'modo_demo': settings.DEMO_MODE,
        'usuario_demo': 'Usuario de demostración' if settings.DEMO_MODE else None,
    }
