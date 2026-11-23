from ..models import Marca


def crear_marca(nombre, descripcion, creado_por):
    if Marca.objects.filter(nombre=nombre).exists():
        raise ValueError(f'Ya existe una marca con el nombre "{nombre}".')
    return Marca.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        creado_por=creado_por,
    )
