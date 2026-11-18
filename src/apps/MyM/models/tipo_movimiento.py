from django.db import models


class TipoMovimiento(models.Model):
    id_tipo_movimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32, unique=True)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'tipo_movimiento'
