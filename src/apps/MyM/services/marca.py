from ..repositories import marca as marca_repo


def crear_marca(nombre, descripcion, usuario):
    return marca_repo.crear_marca(nombre, descripcion, usuario)
