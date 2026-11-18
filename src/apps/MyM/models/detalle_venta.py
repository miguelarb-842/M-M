from decimal import Decimal

from django.db import models
from django.db.models import UniqueConstraint

from .audit import Auditoria, check_auditoria, check_montos


class DetalleVenta(Auditoria):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey('Venta', on_delete=models.PROTECT)
    id_variante = models.ForeignKey('Variante', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=13, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'detalle_venta'
        constraints = [
            UniqueConstraint(fields=['id_venta', 'id_variante'], name='ck_detalle_venta_venta_variante'),
            check_montos('ck_detalle_venta_montos', 'cantidad', 'precio_unitario', 'descuento', 'impuesto', 'subtotal'),
            check_auditoria('ck_detalle_venta_auditoria'),
        ]
