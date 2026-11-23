from decimal import Decimal
from django.db import transaction

from ..repositories import producto as prod_repo
from ..repositories import variante as var_repo
from ..repositories import inventario as inv_repo


def crear_producto_con_variantes(
    id_marca, id_categoria, nombre, descripcion, variantes, usuario,
    stock_inicial=Decimal('0'),
):
    """
    Crea un producto con sus variantes y el registro de inventario de cada una,
    todo en una sola transacción atómica.

    variantes: lista de dicts con claves 'nombre' y opcional 'descripcion'.
    """
    with transaction.atomic():
        producto = prod_repo.crear_producto(
            id_marca, id_categoria, nombre, descripcion, usuario,
        )
        for v in variantes:
            variante = var_repo.crear_variante(
                producto, v['nombre'], v.get('descripcion'), usuario,
            )
            inv_repo.crear_inventario(
                variante, stock_inicial, Decimal('0'), usuario,
            )
    return producto
