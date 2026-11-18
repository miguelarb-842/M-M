from decimal import Decimal

from django.db import models
from django.db.models import UniqueConstraint

from .audit import Auditoria, check_auditoria, check_montos


class DetalleCompra(Auditoria):
    id_detalle_compra = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey('Compra', on_delete=models.PROTECT)
    id_variante = models.ForeignKey('Variante', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'detalle_compra'
        constraints = [
            UniqueConstraint(fields=['id_compra', 'id_variante'], name='ck_detalle_compra_compra_variante'),
            check_montos('ck_detalle_compra_montos', 'cantidad', 'costo_unitario', 'descuento', 'impuesto', 'subtotal'),
            check_auditoria('ck_detalle_compra_auditoria'),
        ]
