from django.db import models

from .audit import Auditoria, check_auditoria


class Producto(Auditoria):
    id_producto = models.AutoField(primary_key=True)
    id_marca = models.ForeignKey('Marca', on_delete=models.PROTECT)
    id_categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=254)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'producto'
        constraints = [check_auditoria('ck_producto_auditoria')]
