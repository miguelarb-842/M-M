from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from ..forms import LoginForm


def iniciar_sesion(request):
    if settings.DEMO_MODE:
        return render(request, 'pages/login.html')
    return LoginView.as_view(
        template_name='pages/login.html',
        authentication_form=LoginForm,
    )(request)


def cerrar_sesion(request):
    if settings.DEMO_MODE:
        return redirect('MyM:inicio')
    return LogoutView.as_view(next_page='MyM:login')(request)
