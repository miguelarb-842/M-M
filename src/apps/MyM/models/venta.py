from decimal import Decimal

from django.db import models

from .audit import Auditoria, check_auditoria, check_montos


class Venta(Auditoria):
    id_venta = models.AutoField(primary_key=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    total = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField()
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'venta'
        constraints = [
            check_montos('ck_venta_montos', 'subtotal', 'descuento', 'impuesto', 'total'),
            check_auditoria('ck_venta_auditoria'),
        ]
