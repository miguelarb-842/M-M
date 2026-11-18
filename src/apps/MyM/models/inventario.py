from decimal import Decimal

from django.db import models
from django.db.models import CheckConstraint, Q

from .audit import Auditoria, check_auditoria, check_montos


class Inventario(Auditoria):
    id_inventario = models.AutoField(primary_key=True)
    id_variante = models.OneToOneField('Variante', on_delete=models.PROTECT)
    stock_actual = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0'))
    stock_minimo = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal('0'))

    class Meta:
        db_table = 'inventario'
        constraints = [
            check_montos('ck_inventario_stock', 'stock_actual', 'stock_minimo'),
            check_auditoria('ck_inventario_auditoria'),
        ]
