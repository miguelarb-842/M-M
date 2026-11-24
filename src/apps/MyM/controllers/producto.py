from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .home import acceso_requerido
from ..forms import ProductoForm, VarianteFormSet
from ..models import Marca, Categoria, Producto, Variante, Inventario
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
                    'stock_minimo': detalle_form.cleaned_data.get('stock_minimo') or Decimal('0'),
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


@acceso_requerido
def editar_producto(request, pk):
    """Edita un producto y sus variantes: actualiza existentes y agrega nuevas."""
    producto = get_object_or_404(Producto, pk=pk)
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
                    'id': detalle_form.cleaned_data.get('id') or None,
                    'nombre': nombre_var,
                    'descripcion': detalle_form.cleaned_data.get('descripcion', '').strip(),
                    'stock_minimo': detalle_form.cleaned_data.get('stock_minimo') or Decimal('0'),
                })

            if not variantes:
                form.add_error(None, 'Debe registrar al menos una variante.')
            else:
                try:
                    producto_service.editar_producto_con_variantes(
                        pk,
                        form.cleaned_data['id_marca'],
                        form.cleaned_data['id_categoria'],
                        form.cleaned_data['nombre'],
                        form.cleaned_data['descripcion'],
                        variantes,
                        request.user,
                    )
                    messages.success(
                        request,
                        f'Producto "{form.cleaned_data["nombre"]}" actualizado.',
                    )
                    return redirect('MyM:detalle_producto', pk=pk)
                except ValueError as e:
                    messages.error(request, str(e))
    else:
        form = ProductoForm(
            initial={
                'nombre': producto.nombre,
                'descripcion': producto.descripcion or '',
                'id_marca': producto.id_marca,
                'id_categoria': producto.id_categoria,
            }
        )
        variantes = Variante.objects.filter(id_producto=producto)
        inventarios = {
            inv.id_variante_id: inv
            for inv in Inventario.objects.filter(id_variante__in=variantes)
        }
        initial = []
        for v in variantes:
            inv = inventarios.get(v.id_variante)
            initial.append({
                'id': v.id_variante,
                'nombre': v.nombre,
                'descripcion': v.descripcion or '',
                'stock_minimo': inv.stock_minimo if inv else Decimal('0'),
            })
        formset = VarianteFormSet(initial=initial)

    return render(request, 'pages/catalogo/registrar_producto.html', {
        'form': form,
        'formset': formset,
        'producto': producto,
        'edicion': True,
    })
