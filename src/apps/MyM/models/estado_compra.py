from django.db import models


class EstadoCompra(models.Model):
    id_estado_compra = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32, unique=True)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'estado_compra'
