from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint

from .audit import Auditoria, check_auditoria


class Variante(Auditoria):
    id_variante = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=128)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'variante'
        constraints = [
            UniqueConstraint(fields=['id_producto', 'nombre'], name='ck_variante_producto_nombre'),
            check_auditoria('ck_variante_auditoria'),
        ]
