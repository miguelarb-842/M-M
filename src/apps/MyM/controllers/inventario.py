from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.utils import timezone

from .home import acceso_requerido
from ..forms import DetalleMovimientoForm, DetalleMovimientoFormSet, MovimientoInventarioForm
from ..services import inventario as inv_service


@acceso_requerido
def inventario(request):
    """Listado de inventarios con su stock actual y mínimo."""
    inventarios = inv_service.listar_inventarios()
    return render(request, 'pages/inventario/listar.html', {'inventarios': inventarios})


@acceso_requerido
def listar_movimientos(request):
    """Listado histórico de movimientos de inventario."""
    movimientos = inv_service.listar_movimientos()
    return render(request, 'pages/inventario/listar_movimientos.html', {'movimientos': movimientos})


@acceso_requerido
def detalle_movimiento(request, movimiento_id):
    """Detalle de un movimiento con sus variantes y cantidades."""
    try:
        movimiento, detalles = inv_service.obtener_movimiento_con_detalles(movimiento_id)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('MyM:listar_movimientos')
    return render(
        request,
        'pages/inventario/detalle_movimiento.html',
        {'movimiento': movimiento, 'detalles': detalles},
    )


@acceso_requerido
def registrar_movimiento(request):
    """Registra un movimiento de inventario con uno o más detalles."""
    if request.method == 'POST':
        form = MovimientoInventarioForm(request.POST, prefix='movimiento')
        formset = DetalleMovimientoFormSet(request.POST, prefix='detalles')
        if form.is_valid() and formset.is_valid():
            try:
                detalles = []
                for detalle_form in formset:
                    if detalle_form.cleaned_data.get('DELETE'):
                        continue
                    variante = detalle_form.cleaned_data.get('variante')
                    cantidad = detalle_form.cleaned_data.get('cantidad')
                    if variante and cantidad is not None:
                        detalles.append({'variante': variante, 'cantidad': cantidad})

                if not detalles:
                    form.add_error(None, 'El movimiento debe tener al menos un detalle.')
                else:
                    inv_service.registrar_movimiento(
                        tipo_movimiento=form.cleaned_data['tipo_movimiento'],
                        fecha=timezone.now(),
                        descripcion=form.cleaned_data['descripcion'],
                        detalles=detalles,
                        usuario=request.user,
                    )
                    messages.success(request, 'Movimiento registrado correctamente.')
                    return redirect('MyM:inventario')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = MovimientoInventarioForm(prefix='movimiento')
        formset = DetalleMovimientoFormSet(prefix='detalles')
    return render(
        request,
        'pages/inventario/registrar_movimiento.html',
        {'form': form, 'formset': formset},
    )
