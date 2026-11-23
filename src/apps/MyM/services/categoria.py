from ..repositories import categoria as categoria_repo


def crear_categoria(nombre, descripcion, usuario):
    return categoria_repo.crear_categoria(nombre, descripcion, usuario)
