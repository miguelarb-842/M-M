from django.shortcuts import render, get_object_or_404

from .home import acceso_requerido
from ..models import Producto, Variante, Inventario


@acceso_requerido
def catalogo(request):
    """Listado de productos con su marca y categoría."""
    productos = Producto.objects.select_related(
        'id_marca', 'id_categoria',
    ).order_by('-fecha_creacion')
    return render(request, 'pages/catalogo/listar.html', {'productos': productos})


@acceso_requerido
def detalle_producto(request, pk):
    """Detalle de un producto: descripción, marca, categoría y variantes con inventario."""
    producto = get_object_or_404(
        Producto.objects.select_related('id_marca', 'id_categoria'),
        pk=pk,
    )
    variantes = Variante.objects.filter(id_producto=producto)
    inventarios = {
        inv.id_variante_id: inv
        for inv in Inventario.objects.filter(id_variante__in=variantes)
    }
    return render(request, 'pages/catalogo/detalle.html', {
        'producto': producto,
        'variantes': variantes,
        'inventarios': inventarios,
    })
