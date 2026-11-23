from ..models import Producto


def crear_producto(id_marca, id_categoria, nombre, descripcion, creado_por):
    return Producto.objects.create(
        id_marca=id_marca,
        id_categoria=id_categoria,
        nombre=nombre,
        descripcion=descripcion,
        creado_por=creado_por,
    )
