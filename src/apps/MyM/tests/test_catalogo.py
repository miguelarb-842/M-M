"""Pruebas del servicio de catálogo: marcas, categorías, productos y variantes."""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import transaction

from apps.MyM.models import (
    Marca, Categoria, Producto, Variante, Inventario,
)
from apps.MyM.services import marca as marca_service
from apps.MyM.services import categoria as categoria_service
from apps.MyM.services import producto as producto_service


class CatalogoServiceTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.usuario = self.User.objects.create_user(
            nombre='catalogo_admin', password='Clave123',
        )

    # --- Marcas ---

    def test_crear_marca(self):
        """Se puede crear una marca con nombre y descripción."""
        marca = marca_service.crear_marca(
            'Marca A', 'Descripción marca A', self.usuario,
        )
        self.assertEqual(marca.nombre, 'Marca A')
        self.assertEqual(marca.descripcion, 'Descripción marca A')
        self.assertEqual(marca.creado_por, self.usuario)

    def test_marca_duplicada_rechaza(self):
        """Crear una marca con nombre duplicado lanza ValueError."""
        marca_service.crear_marca('Marca A', 'Desc', self.usuario)
        with self.assertRaises(ValueError):
            marca_service.crear_marca('Marca A', 'Otra desc', self.usuario)

    # --- Categorías ---

    def test_crear_categoria(self):
        """Se puede crear una categoría con nombre y descripción."""
        categoria = categoria_service.crear_categoria(
            'Categoria A', 'Descripción categoria A', self.usuario,
        )
        self.assertEqual(categoria.nombre, 'Categoria A')
        self.assertEqual(categoria.descripcion, 'Descripción categoria A')
        self.assertEqual(categoria.creado_por, self.usuario)

    def test_categoria_duplicada_rechaza(self):
        """Crear una categoría con nombre duplicado lanza ValueError."""
        categoria_service.crear_categoria('Categoria A', 'Desc', self.usuario)
        with self.assertRaises(ValueError):
            categoria_service.crear_categoria('Categoria A', 'Otra desc', self.usuario)

    # --- Productos con variantes ---

    def test_crear_producto_con_variantes(self):
        """Se crea producto con múltiples variantes e inventario en una transacción."""
        marca = Marca.objects.create(nombre='Marca X', creado_por=self.usuario)
        categoria = Categoria.objects.create(nombre='Categoria X', creado_por=self.usuario)

        producto = producto_service.crear_producto_con_variantes(
            marca, categoria, 'Laptop', 'Laptop de prueba',
            [
                {'nombre': '14 pulgadas', 'descripcion': 'Pantalla 14"', 'stock_minimo': Decimal('5')},
                {'nombre': '16 pulgadas', 'descripcion': 'Pantalla 16"', 'stock_minimo': Decimal('10')},
            ],
            self.usuario,
        )

        self.assertEqual(producto.nombre, 'Laptop')
        self.assertEqual(producto.id_marca, marca)
        self.assertEqual(producto.id_categoria, categoria)
        self.assertEqual(producto.creado_por, self.usuario)

        variantes = Variante.objects.filter(id_producto=producto)
        self.assertEqual(variantes.count(), 2)
        self.assertTrue(variantes.filter(nombre='14 pulgadas').exists())
        self.assertTrue(variantes.filter(nombre='16 pulgadas').exists())

        # Cada variante tiene su registro de inventario con su stock mínimo
        stock_por_variante = {
            '14 pulgadas': Decimal('5'),
            '16 pulgadas': Decimal('10'),
        }
        for variante in variantes:
            inventario = Inventario.objects.get(id_variante=variante)
            self.assertEqual(inventario.stock_actual, Decimal('0'))
            self.assertEqual(inventario.stock_minimo, stock_por_variante[variante.nombre])
            self.assertEqual(inventario.creado_por, self.usuario)

    def test_stock_minimo_por_defecto_es_cero(self):
        """Si no se indica stock mínimo, el inventario de la variante queda en 0."""
        marca = Marca.objects.create(nombre='Marca Z', creado_por=self.usuario)
        categoria = Categoria.objects.create(nombre='Categoria Z', creado_por=self.usuario)

        producto = producto_service.crear_producto_con_variantes(
            marca, categoria, 'Teclado', 'Teclado mecánico',
            [{'nombre': 'Español', 'descripcion': 'Layout ES'}],
            self.usuario,
        )

        inventario = Inventario.objects.get(id_variante__id_producto=producto)
        self.assertEqual(inventario.stock_minimo, Decimal('0'))
        self.assertEqual(inventario.stock_actual, Decimal('0'))

    def test_editar_producto_con_variantes(self):
        """Se edita producto, variantes existentes y se agregan nuevas sin eliminar."""
        marca = Marca.objects.create(nombre='Marca E', creado_por=self.usuario)
        categoria = Categoria.objects.create(nombre='Categoria E', creado_por=self.usuario)

        producto = producto_service.crear_producto_con_variantes(
            marca, categoria, 'Monitor', 'Monitor LED',
            [{'nombre': '24 pulgadas', 'descripcion': 'Full HD', 'stock_minimo': Decimal('3')}],
            self.usuario,
        )
        variante = Variante.objects.get(id_producto=producto, nombre='24 pulgadas')

        producto_service.editar_producto_con_variantes(
            producto.id_producto,
            marca, categoria, 'Monitor Pro', 'Monitor profesional',
            [
                {'id': variante.id_variante, 'nombre': '24 pulgadas', 'descripcion': 'Full HD IPS', 'stock_minimo': Decimal('8')},
                {'nombre': '27 pulgadas', 'descripcion': '4K', 'stock_minimo': Decimal('5')},
            ],
            self.usuario,
        )

        producto.refresh_from_db()
        self.assertEqual(producto.nombre, 'Monitor Pro')
        self.assertEqual(producto.descripcion, 'Monitor profesional')

        variantes = Variante.objects.filter(id_producto=producto)
        self.assertEqual(variantes.count(), 2)
        self.assertTrue(variantes.filter(nombre='24 pulgadas').exists())
        self.assertTrue(variantes.filter(nombre='27 pulgadas').exists())

        self.assertEqual(
            Inventario.objects.get(id_variante__nombre='24 pulgadas').stock_minimo,
            Decimal('8'),
        )
        self.assertEqual(
            Inventario.objects.get(id_variante__nombre='27 pulgadas').stock_minimo,
            Decimal('5'),
        )
        self.assertEqual(
            Inventario.objects.get(id_variante__nombre='27 pulgadas').stock_actual,
            Decimal('0'),
        )

    def test_producto_con_una_variante(self):
        """Se puede crear un producto con una sola variante."""
        marca = Marca.objects.create(nombre='Marca Y', creado_por=self.usuario)
        categoria = Categoria.objects.create(nombre='Categoria Y', creado_por=self.usuario)

        producto = producto_service.crear_producto_con_variantes(
            marca, categoria, 'Mouse', 'Mouse inalámbrico',
            [{'nombre': 'Estándar'}],
            self.usuario,
        )

        variantes = Variante.objects.filter(id_producto=producto)
        self.assertEqual(variantes.count(), 1)
        self.assertEqual(variantes.get().nombre, 'Estándar')

    def test_variante_mismo_nombre_distinto_producto_permitido(self):
        """El mismo nombre de variante sí se permite en productos diferentes."""
        marca = Marca.objects.create(nombre='Marca W', creado_por=self.usuario)
        categoria = Categoria.objects.create(nombre='Categoria W', creado_por=self.usuario)

        producto_service.crear_producto_con_variantes(
            marca, categoria, 'Producto A', 'Desc',
            [{'nombre': 'Talla M'}],
            self.usuario,
        )
        producto_service.crear_producto_con_variantes(
            marca, categoria, 'Producto B', 'Desc',
            [{'nombre': 'Talla M'}],
            self.usuario,
        )

        self.assertEqual(
            Variante.objects.filter(nombre='Talla M').count(), 2
        )

    def test_variante_duplicada_dentro_mismo_llamada_hace_rollback(self):
        """Si una lista trae dos variantes con el mismo nombre, la transacción revierte todo."""
        marca = Marca.objects.create(nombre='Marca R', creado_por=self.usuario)
        categoria = Categoria.objects.create(nombre='Categoria R', creado_por=self.usuario)

        productos_antes = Producto.objects.count()
        variantes_antes = Variante.objects.count()
        inventarios_antes = Inventario.objects.count()

        with self.assertRaises(ValueError):
            producto_service.crear_producto_con_variantes(
                marca, categoria, 'Producto R', 'Desc',
                [
                    {'nombre': 'Talla M'},
                    {'nombre': 'Talla M'},  # duplicada dentro del mismo producto
                ],
                self.usuario,
            )

        # Rollback completo: nada se guardó
        self.assertEqual(Producto.objects.count(), productos_antes)
        self.assertEqual(Variante.objects.count(), variantes_antes)
        self.assertEqual(Inventario.objects.count(), inventarios_antes)
