from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils import timezone


class Auditoria(models.Model):
    # bloque de auditoría repetido en el esquema SQL
    creado_por = models.ForeignKey('Usuario', on_delete=models.PROTECT, related_name='+')
    # se llena sola al crear (DEFAULT CURRENT_TIMESTAMP en el esquema SQL)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # se llena sola en cada save() de un registro existente (SQLite no tiene ON UPDATE)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True, editable=False)
    actualizado_por = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=True, blank=True, related_name='+', editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # en guardados completos de un registro existente, se exige quién actualiza;
        # los guardados parciales internos (last_login del login) pasan sin tocar auditoría
        if self.pk and kwargs.get('update_fields') is None:
            if self.actualizado_por is None:
                raise ValueError('actualizado_por es requerido al actualizar un registro')
            self.fecha_actualizacion = timezone.now()
        super().save(*args, **kwargs)


def check_auditoria(nombre):
    # (ambos nulos) o (ambos presentes), como el CHECK del esquema
    return CheckConstraint(
        condition=Q(fecha_actualizacion__isnull=True, actualizado_por__isnull=True)
              | Q(fecha_actualizacion__isnull=False, actualizado_por__isnull=False),
        name=nombre,
    )


def check_montos(nombre, *campos):
    return CheckConstraint(
        condition=Q(**{f'{c}__gte': 0 for c in campos}),
        name=nombre,
    )
