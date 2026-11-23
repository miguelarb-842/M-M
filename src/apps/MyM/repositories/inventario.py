from decimal import Decimal

from django.db import IntegrityError

from ..models import DetalleMovimiento, Inventario, MovimientoInventario, TipoMovimiento


def obtener_inventario_por_variante(variante_id):
    return Inventario.objects.filter(id_variante=variante_id).first()


def obtener_o_crear_inventario_bloqueado(variante, creado_por):
    """
    Obtiene el inventario con bloqueo SELECT FOR UPDATE; si no existe, lo crea con stock 0.
    Debe llamarse dentro de una transacción (transaction.atomic).
    Maneja race condition: si dos transacciones crean simultáneamente, la segunda
    captura el IntegrityError y lee la fila creada por la primera con bloqueo.
    """
    try:
        return Inventario.objects.select_for_update().get(id_variante=variante), False
    except Inventario.DoesNotExist:
        try:
            return (
                Inventario.objects.create(
                    id_variante=variante,
                    stock_actual=Decimal('0'),
                    stock_minimo=Decimal('0'),
                    creado_por=creado_por,
                ),
                True,
            )
        except IntegrityError:
            # Otra transacción creó la fila entre el get y el create.
            return Inventario.objects.select_for_update().get(id_variante=variante), False


def crear_inventario(variante, stock_actual, stock_minimo, creado_por):
    return Inventario.objects.create(
        id_variante=variante,
        stock_actual=stock_actual,
        stock_minimo=stock_minimo,
        creado_por=creado_por,
    )


def editar_inventario(inventario, stock_actual=None, stock_minimo=None, actualizado_por=None):
    if actualizado_por is None:
        raise ValueError('actualizado_por es requerido al editar un inventario')
    if stock_actual is not None:
        inventario.stock_actual = stock_actual
    if stock_minimo is not None:
        inventario.stock_minimo = stock_minimo
    inventario.actualizado_por = actualizado_por
    inventario.save()
    return inventario


def obtener_tipo_movimiento_por_nombre(nombre):
    try:
        return TipoMovimiento.objects.get(nombre=nombre)
    except TipoMovimiento.DoesNotExist:
        raise ValueError(f"Tipo de movimiento '{nombre}' no existe")


def listar_inventarios():
    return Inventario.objects.select_related('id_variante').all()


def crear_movimiento(tipo_movimiento, fecha, descripcion, creado_por, id_compra=None, id_venta=None):
    if id_compra is not None:
        from ..models import Compra

        if not Compra.objects.filter(pk=id_compra).exists():
            raise ValueError(f'Compra con id {id_compra} no existe')
    if id_venta is not None:
        from ..models import Venta

        if not Venta.objects.filter(pk=id_venta).exists():
            raise ValueError(f'Venta con id {id_venta} no existe')
    return MovimientoInventario.objects.create(
        id_tipo_movimiento=tipo_movimiento,
        fecha=fecha,
        descripcion=descripcion,
        creado_por=creado_por,
        id_compra=id_compra,
        id_venta=id_venta,
    )


def agregar_detalle(movimiento, variante, cantidad, creado_por):
    if cantidad is None or cantidad < 0:
        raise ValueError('La cantidad debe ser un número mayor o igual a cero')
    return DetalleMovimiento.objects.create(
        id_movimiento_inventario=movimiento,
        id_variante=variante,
        cantidad=cantidad,
        creado_por=creado_por,
    )
