from django.db import transaction
from django.utils import timezone

from ..repositories import inventario as inv_repo


TIPOS_QUE_SUMA_STOCK = {'entrada', 'ajuste positivo'}
TIPOS_QUE_RESTA_STOCK = {'salida', 'ajuste negativo'}


def _nombre_tipo(tipo_movimiento):
    if hasattr(tipo_movimiento, 'nombre'):
        return tipo_movimiento.nombre
    return tipo_movimiento


def _resolver_tipo(tipo_movimiento):
    if hasattr(tipo_movimiento, 'nombre'):
        return tipo_movimiento
    return inv_repo.obtener_tipo_movimiento_por_nombre(tipo_movimiento)


def crear_inventario(variante, stock_actual, stock_minimo, creado_por):
    return inv_repo.crear_inventario(variante, stock_actual, stock_minimo, creado_por)


def editar_inventario(inventario, stock_actual=None, stock_minimo=None, actualizado_por=None):
    return inv_repo.editar_inventario(inventario, stock_actual, stock_minimo, actualizado_por)


def obtener_inventario_por_variante(variante_id):
    return inv_repo.obtener_inventario_por_variante(variante_id)


def listar_inventarios():
    return inv_repo.listar_inventarios()


def registrar_movimiento(tipo_movimiento, fecha, descripcion, detalles, usuario, id_compra=None, id_venta=None):
    """
    Registra un movimiento de inventario con sus detalles y actualiza el stock automáticamente.

    detalles: lista de dicts con claves 'variante' (objeto Variante) y 'cantidad' (Decimal).
    tipo_movimiento: objeto TipoMovimiento o nombre de tipo ('entrada', 'salida', etc.).
    usuario: objeto Usuario que ejecuta el movimiento (llena creado_por y actualizado_por).
    """
    if not detalles:
        raise ValueError('El movimiento debe tener al menos un detalle')

    if fecha is None:
        fecha = timezone.now()
    elif hasattr(fecha, 'utcoffset') and fecha.utcoffset() is None:
        fecha = timezone.make_aware(fecha)

    tipo_nombre = _nombre_tipo(tipo_movimiento)
    tipo_obj = _resolver_tipo(tipo_movimiento)

    with transaction.atomic():
        movimiento = inv_repo.crear_movimiento(
            tipo_movimiento=tipo_obj,
            fecha=fecha,
            descripcion=descripcion,
            creado_por=usuario,
            id_compra=id_compra,
            id_venta=id_venta,
        )

        for detalle in detalles:
            variante = detalle['variante']
            cantidad = detalle['cantidad']

            inventario, _ = inv_repo.obtener_o_crear_inventario_bloqueado(variante, usuario)

            if tipo_nombre in TIPOS_QUE_RESTA_STOCK:
                if inventario.stock_actual - cantidad < 0:
                    raise ValueError(
                        f'Stock insuficiente para la variante {variante.nombre}. '
                        f'Disponible: {inventario.stock_actual}, solicitado: {cantidad}'
                    )

            inv_repo.agregar_detalle(
                movimiento=movimiento,
                variante=variante,
                cantidad=cantidad,
                creado_por=usuario,
            )

            if tipo_nombre in TIPOS_QUE_SUMA_STOCK:
                inventario.stock_actual += cantidad
            else:
                inventario.stock_actual -= cantidad

            inventario.actualizado_por = usuario
            inventario.save()

        return movimiento
