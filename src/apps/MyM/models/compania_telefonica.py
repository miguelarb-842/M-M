from django.db import models


class CompaniaTelefonica(models.Model):
    id_compania_telefonica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = 'compania_telefonica'
