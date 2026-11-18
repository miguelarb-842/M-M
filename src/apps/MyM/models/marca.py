from django.db import models

from .audit import Auditoria, check_auditoria


class Marca(Auditoria):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, unique=True)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'marca'
        constraints = [check_auditoria('ck_marca_auditoria')]
