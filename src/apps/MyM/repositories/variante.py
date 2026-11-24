from ..models import Variante


def crear_variante(id_producto, nombre, descripcion, creado_por):
    if Variante.objects.filter(id_producto=id_producto, nombre=nombre).exists():
        raise ValueError(
            f'Ya existe una variante con el nombre "{nombre}" para este producto.'
        )
    return Variante.objects.create(
        id_producto=id_producto,
        nombre=nombre,
        descripcion=descripcion,
        creado_por=creado_por,
    )


def actualizar_variante(variante, nombre, descripcion, actualizado_por):
    if Variante.objects.filter(
        id_producto=variante.id_producto, nombre=nombre
    ).exclude(pk=variante.pk).exists():
        raise ValueError(
            f'Ya existe una variante con el nombre "{nombre}" para este producto.'
        )
    variante.nombre = nombre
    variante.descripcion = descripcion
    variante.actualizado_por = actualizado_por
    variante.save()
    return variante
