from django.contrib.auth import authenticate as django_authenticate, login as django_login, logout as django_logout


def autenticar(identifier, password, request=None):
    """
    Intenta autenticar al usuario por nombre de usuario.
    Devuelve el Usuario o None.
    """
    return django_authenticate(request, username=identifier, password=password)


def iniciar_sesion(request, user):
    django_login(request, user)


def cerrar_sesion(request):
    django_logout(request)
