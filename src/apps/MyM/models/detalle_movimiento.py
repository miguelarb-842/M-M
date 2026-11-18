from decimal import Decimal

from django.db import models
from django.db.models import UniqueConstraint

from .audit import Auditoria, check_auditoria, check_montos


class DetalleMovimiento(Auditoria):
    id_detalle_movimiento = models.AutoField(primary_key=True)
    id_movimiento_inventario = models.ForeignKey('MovimientoInventario', on_delete=models.PROTECT)
    id_variante = models.ForeignKey('Variante', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'detalle_movimiento'
        constraints = [
            UniqueConstraint(fields=['id_movimiento_inventario', 'id_variante'], name='ck_detalle_movimiento_mov_variante'),
            check_montos('ck_detalle_movimiento_montos', 'cantidad'),
            check_auditoria('ck_detalle_movimiento_auditoria'),
        ]
