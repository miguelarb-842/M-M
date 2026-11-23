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
