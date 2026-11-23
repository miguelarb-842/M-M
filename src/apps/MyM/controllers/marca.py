from django.contrib import messages
from django.shortcuts import redirect, render

from .home import acceso_requerido
from ..forms import MarcaForm
from ..services import marca as marca_service


@acceso_requerido
def registrar_marca(request):
    """Registra una nueva marca."""
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            try:
                marca_service.crear_marca(
                    form.cleaned_data['nombre'],
                    form.cleaned_data['descripcion'],
                    request.user,
                )
                messages.success(
                    request,
                    f'Marca "{form.cleaned_data["nombre"]}" registrada correctamente.',
                )
                return redirect('MyM:registrar_marca')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = MarcaForm()
    return render(request, 'pages/catalogo/registrar_marca.html', {'form': form})
