<!--

Realizado: Miguel Gutierrez
Es una pequeña muestra okey falta mas
 -->


# Sistema gestor de inventario para la Librería M&M

Proyecto Integrador del curso Fundamentos de Programación con Python.

## Descripción

Prototipo de un sistema gestor de inventario para la Librería M&M, un negocio familiar de Managua que hoy controla sus existencias, compras y precios de forma manual. El sistema permite registrar productos y variantes, controlar existencias, registrar compras, ventas y movimientos de inventario, y consultar la información desde una interfaz web básica.

## Tecnologías

- Python
- SQLite
- Django

## Estado del proyecto

En desarrollo. El diagnóstico, el análisis y el diseño de la base de datos están completos. La lógica en Python y la interfaz web están en preparación.

## Modelo de datos

La base de datos tiene 17 tablas agrupadas en administración, catálogo, operaciones e inventario. La variante es la unidad que se compra, se vende y se controla en el inventario. Los diagramas del modelo se encuentran en la sección 5 del documento del proyecto.

## Convenciones de nombres

- Clases y tablas: PascalCase (por ejemplo, `Producto`, `DetalleVenta`).
- Variables, campos, funciones y parámetros: snake_case (por ejemplo, `precio_sugerido`, `registrar_producto()`).
- Constantes: MAYÚSCULAS_CON_GUIONES_BAJOS (por ejemplo, `MARGEN_GANANCIA = 0.15`).

Estas convenciones aplican al desarrollo del proyecto académico.