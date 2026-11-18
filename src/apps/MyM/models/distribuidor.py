from django.db import models

from .audit import Auditoria, check_auditoria


class Distribuidor(Auditoria):
    id_distribuidor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.CharField(max_length=254, null=True, blank=True)
    correo_electronico = models.CharField(max_length=254, unique=True, null=True, blank=True)
    numero_telefonico = models.CharField(max_length=32, null=True, blank=True)
    codigo_telefonico = models.CharField(max_length=4, default='505')
    id_compania_telefonica = models.ForeignKey('CompaniaTelefonica', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'distribuidor'
        constraints = [check_auditoria('ck_distribuidor_auditoria')]
