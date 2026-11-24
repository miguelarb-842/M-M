from decimal import Decimal
from django.db import transaction

from ..models import Producto, Variante, Inventario
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

    variantes: lista de dicts con claves 'nombre', opcional 'descripcion' y
    opcional 'stock_minimo' (default 0).
    """
    with transaction.atomic():
        producto = prod_repo.crear_producto(
            id_marca, id_categoria, nombre, descripcion, usuario,
        )
        for v in variantes:
            variante = var_repo.crear_variante(
                producto, v['nombre'], v.get('descripcion'), usuario,
            )
            stock_minimo = v.get('stock_minimo') or Decimal('0')
            inv_repo.crear_inventario(
                variante, stock_inicial, stock_minimo, usuario,
            )
    return producto


def editar_producto_con_variantes(
    pk, id_marca, id_categoria, nombre, descripcion, variantes, usuario,
):
    """
    Actualiza un producto, sus variantes existentes y crea las nuevas.
    No elimina variantes.

    variantes: lista de dicts con claves opcional 'id', 'nombre',
    'descripcion' y 'stock_minimo' (default 0).
    """
    with transaction.atomic():
        producto = Producto.objects.get(pk=pk)
        producto = prod_repo.actualizar_producto(
            producto, id_marca, id_categoria, nombre, descripcion, usuario,
        )

        variantes_existentes = {
            v.id_variante: v
            for v in Variante.objects.filter(id_producto=producto)
        }
        ids_existentes = set(variantes_existentes.keys())
        inventarios_existentes = {
            inv.id_variante_id: inv
            for inv in Inventario.objects.filter(id_variante__in=ids_existentes)
        }

        for v in variantes:
            vid = v.get('id')
            stock_minimo = v.get('stock_minimo') or Decimal('0')
            if vid and vid in variantes_existentes:
                variante = variantes_existentes[vid]
                var_repo.actualizar_variante(
                    variante, v['nombre'], v.get('descripcion', ''), usuario,
                )
                inventario = inventarios_existentes.get(vid)
                if inventario is None:
                    inv_repo.crear_inventario(
                        variante, Decimal('0'), stock_minimo, usuario,
                    )
                else:
                    inv_repo.editar_inventario(
                        inventario,
                        stock_minimo=stock_minimo,
                        actualizado_por=usuario,
                    )
            else:
                variante = var_repo.crear_variante(
                    producto, v['nombre'], v.get('descripcion', ''), usuario,
                )
                inv_repo.crear_inventario(
                    variante, Decimal('0'), stock_minimo, usuario,
                )
    return producto
