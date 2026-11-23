from ..models import Categoria


def crear_categoria(nombre, descripcion, creado_por):
    if Categoria.objects.filter(nombre=nombre).exists():
        raise ValueError(f'Ya existe una categoría con el nombre "{nombre}".')
    return Categoria.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        creado_por=creado_por,
    )
