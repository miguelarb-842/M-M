from django.contrib import messages
from django.shortcuts import redirect, render

from .home import acceso_requerido
from ..forms import CategoriaForm
from ..services import categoria as categoria_service


@acceso_requerido
def registrar_categoria(request):
    """Registra una nueva categoría."""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            try:
                categoria_service.crear_categoria(
                    form.cleaned_data['nombre'],
                    form.cleaned_data['descripcion'],
                    request.user,
                )
                messages.success(
                    request,
                    f'Categoría "{form.cleaned_data["nombre"]}" registrada correctamente.',
                )
                return redirect('MyM:registrar_categoria')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = CategoriaForm()
    return render(request, 'pages/catalogo/registrar_categoria.html', {'form': form})
