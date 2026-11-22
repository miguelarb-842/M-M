from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone

from .audit import Auditoria, check_auditoria


class MovimientoInventario(Auditoria):
    id_movimiento_inventario = models.AutoField(primary_key=True)
    id_tipo_movimiento = models.ForeignKey('TipoMovimiento', on_delete=models.PROTECT)
    id_compra = models.ForeignKey('Compra', on_delete=models.PROTECT, null=True, blank=True)
    id_venta = models.ForeignKey('Venta', on_delete=models.PROTECT, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'movimiento_inventario'
        constraints = [
            CheckConstraint(
                condition=Q(id_compra__isnull=True) | Q(id_venta__isnull=True),
                name='ck_movimiento_inventario_compra_o_venta',
            ),
            check_auditoria('ck_movimiento_inventario_auditoria'),
        ]
