from decimal import Decimal

from django.db import models

from .audit import Auditoria, check_auditoria, check_montos


class Compra(Auditoria):
    id_compra = models.AutoField(primary_key=True)
    id_distribuidor = models.ForeignKey('Distribuidor', on_delete=models.PROTECT)
    id_estado_compra = models.ForeignKey('EstadoCompra', on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    total = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField()
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'compra'
        constraints = [
            check_montos('ck_compra_montos', 'subtotal', 'descuento', 'impuesto', 'total'),
            check_auditoria('ck_compra_auditoria'),
        ]
