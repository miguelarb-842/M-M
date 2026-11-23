from django.contrib import messages
from django.shortcuts import redirect, render

from .home import acceso_requerido
from ..forms import ProductoForm, VarianteFormSet
from ..models import Marca, Categoria
from ..services import producto as producto_service


@acceso_requerido
def registrar_producto(request):
    """Registra un producto con una o más variantes (transacción atómica)."""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        formset = VarianteFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            variantes = []
            for detalle_form in formset:
                if detalle_form.cleaned_data.get('DELETE'):
                    continue
                nombre_var = detalle_form.cleaned_data.get('nombre', '').strip()
                if not nombre_var:
                    continue
                variantes.append({
                    'nombre': nombre_var,
                    'descripcion': detalle_form.cleaned_data.get('descripcion', '').strip(),
                })

            if not variantes:
                form.add_error(None, 'Debe registrar al menos una variante.')
            else:
                try:
                    producto_service.crear_producto_con_variantes(
                        form.cleaned_data['id_marca'],
                        form.cleaned_data['id_categoria'],
                        form.cleaned_data['nombre'],
                        form.cleaned_data['descripcion'],
                        variantes,
                        request.user,
                    )
                    messages.success(
                        request,
                        f'Producto "{form.cleaned_data["nombre"]}" registrado con {len(variantes)} variante(s).',
                    )
                    return redirect('MyM:registrar_producto')
                except ValueError as e:
                    messages.error(request, str(e))
    else:
        form = ProductoForm()
        formset = VarianteFormSet()

    return render(request, 'pages/catalogo/registrar_producto.html', {
        'form': form,
        'formset': formset,
    })
