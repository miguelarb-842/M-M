from django.conf import settings
from django.shortcuts import redirect, render

from ..forms import LoginForm
from ..services import auth as auth_service


def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth_service.autenticar(identifier, password, request=request)
            if user is not None:
                auth_service.iniciar_sesion(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})


def cerrar_sesion(request):
    auth_service.cerrar_sesion(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
