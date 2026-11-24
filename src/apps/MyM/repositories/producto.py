from ..models import Producto


def crear_producto(id_marca, id_categoria, nombre, descripcion, creado_por):
    return Producto.objects.create(
        id_marca=id_marca,
        id_categoria=id_categoria,
        nombre=nombre,
        descripcion=descripcion,
        creado_por=creado_por,
    )


def actualizar_producto(producto, id_marca, id_categoria, nombre, descripcion, actualizado_por):
    producto.id_marca = id_marca
    producto.id_categoria = id_categoria
    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.actualizado_por = actualizado_por
    producto.save()
    return producto
