"""Pruebas del servicio de inventario: CRUD, movimientos, stock y transaccionalidad."""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.MyM.models import (
    Variante, Producto, Marca, Categoria, TipoMovimiento,
    Inventario, MovimientoInventario, DetalleMovimiento,
)
from apps.MyM.services import inventario as inv_service


class InventarioServiceTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.usuario = self.User.objects.create_user(
            nombre='almacenista',
            password='Clave123',
        )
        self.marca = Marca.objects.create(
            nombre='Marca A', creado_por=self.usuario,
        )
        self.categoria = Categoria.objects.create(
            nombre='Categoria A', creado_por=self.usuario,
        )
        self.producto = Producto.objects.create(
            nombre='Producto X', id_marca=self.marca,
            id_categoria=self.categoria, creado_por=self.usuario,
        )
        self.variante = Variante.objects.create(
            id_producto=self.producto, nombre='Variante 1', creado_por=self.usuario,
        )
        self.tipo_entrada = TipoMovimiento.objects.get(nombre='entrada')
        self.tipo_salida = TipoMovimiento.objects.get(nombre='salida')
        self.tipo_ajuste_pos = TipoMovimiento.objects.get(nombre='ajuste positivo')
        self.tipo_ajuste_neg = TipoMovimiento.objects.get(nombre='ajuste negativo')

    # --- CRUD de inventario ---

    def test_crear_inventario(self):
        """Se puede crear un registro de inventario para una variante."""
        inventario = inv_service.crear_inventario(
            self.variante, Decimal('100'), Decimal('10'), self.usuario,
        )
        self.assertEqual(inventario.stock_actual, Decimal('100'))
        self.assertEqual(inventario.stock_minimo, Decimal('10'))
        self.assertEqual(inventario.creado_por, self.usuario)

    def test_editar_inventario(self):
        """Se puede editar stock_actual y stock_minimo de un inventario existente."""
        inventario = inv_service.crear_inventario(
            self.variante, Decimal('100'), Decimal('10'), self.usuario,
        )
        actualizado = inv_service.editar_inventario(
            inventario,
            stock_actual=Decimal('200'),
            stock_minimo=Decimal('20'),
            actualizado_por=self.usuario,
        )
        self.assertEqual(actualizado.stock_actual, Decimal('200'))
        self.assertEqual(actualizado.stock_minimo, Decimal('20'))
        self.assertEqual(actualizado.actualizado_por, self.usuario)

    def test_obtener_inventario_por_variante(self):
        """Se obtiene el inventario asociado a una variante."""
        inv_service.crear_inventario(
            self.variante, Decimal('50'), Decimal('5'), self.usuario,
        )
        obtenido = inv_service.obtener_inventario_por_variante(self.variante.id_variante)
        self.assertIsNotNone(obtenido)
        self.assertEqual(obtenido.id_variante, self.variante)

    def test_listar_inventarios(self):
        """listar_inventarios devuelve todos los registros con variante relacionada."""
        inv_service.crear_inventario(
            self.variante, Decimal('10'), Decimal('5'), self.usuario,
        )
        resultados = inv_service.listar_inventarios()
        self.assertTrue(any(r.id_variante_id == self.variante.id_variante for r in resultados))

    # --- Movimientos de inventario ---

    def test_registro_entrada_suma_stock(self):
        """Una entrada suma la cantidad al stock_actual."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        movimiento = inv_service.registrar_movimiento(
            self.tipo_entrada,
            '2026-11-22 10:00:00',
            'Entrada de prueba',
            [{'variante': self.variante, 'cantidad': Decimal('5')}],
            self.usuario,
        )
        inventario = Inventario.objects.get(id_variante=self.variante)
        self.assertEqual(inventario.stock_actual, Decimal('15'))
        self.assertEqual(movimiento.id_tipo_movimiento, self.tipo_entrada)

    def test_registro_salida_resta_stock(self):
        """Una salida resta la cantidad del stock_actual."""
        inv_service.crear_inventario(self.variante, Decimal('20'), Decimal('5'), self.usuario)
        movimiento = inv_service.registrar_movimiento(
            self.tipo_salida,
            '2026-11-22 11:00:00',
            'Salida de prueba',
            [{'variante': self.variante, 'cantidad': Decimal('8')}],
            self.usuario,
        )
        inventario = Inventario.objects.get(id_variante=self.variante)
        self.assertEqual(inventario.stock_actual, Decimal('12'))
        self.assertEqual(movimiento.id_tipo_movimiento, self.tipo_salida)

    def test_ajuste_positivo_suma_stock(self):
        """Ajuste positivo suma al stock."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        inv_service.registrar_movimiento(
            self.tipo_ajuste_pos,
            '2026-11-22 12:00:00',
            'Ajuste positivo',
            [{'variante': self.variante, 'cantidad': Decimal('7')}],
            self.usuario,
        )
        inventario = Inventario.objects.get(id_variante=self.variante)
        self.assertEqual(inventario.stock_actual, Decimal('17'))

    def test_ajuste_negativo_resta_stock(self):
        """Ajuste negativo resta del stock."""
        inv_service.crear_inventario(self.variante, Decimal('20'), Decimal('5'), self.usuario)
        inv_service.registrar_movimiento(
            self.tipo_ajuste_neg,
            '2026-11-22 13:00:00',
            'Ajuste negativo',
            [{'variante': self.variante, 'cantidad': Decimal('5')}],
            self.usuario,
        )
        inventario = Inventario.objects.get(id_variante=self.variante)
        self.assertEqual(inventario.stock_actual, Decimal('15'))

    def test_tipo_movimiento_como_string_funciona(self):
        """Se puede pasar el tipo de movimiento como string en lugar de objeto."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        movimiento = inv_service.registrar_movimiento(
            'entrada',
            '2026-11-22 14:00:00',
            'Tipo como string',
            [{'variante': self.variante, 'cantidad': Decimal('3')}],
            self.usuario,
        )
        inventario = Inventario.objects.get(id_variante=self.variante)
        self.assertEqual(inventario.stock_actual, Decimal('13'))
        self.assertEqual(movimiento.id_tipo_movimiento.nombre, 'entrada')

    def test_stock_insuficiente_rechaza(self):
        """Una salida mayor al stock disponible lanza ValueError y no guarda nada."""
        inv_service.crear_inventario(self.variante, Decimal('5'), Decimal('0'), self.usuario)
        stock_antes = Inventario.objects.get(id_variante=self.variante).stock_actual
        movimientos_antes = MovimientoInventario.objects.count()

        with self.assertRaises(ValueError):
            inv_service.registrar_movimiento(
                self.tipo_salida,
                '2026-11-22 15:00:00',
                'Salida invalida',
                [{'variante': self.variante, 'cantidad': Decimal('999')}],
                self.usuario,
            )

        # Nada se guardó parcialmente
        stock_despues = Inventario.objects.get(id_variante=self.variante).stock_actual
        movimientos_despues = MovimientoInventario.objects.count()
        self.assertEqual(stock_antes, stock_despues)
        self.assertEqual(movimientos_antes, movimientos_despues)

    def test_crear_inventario_automatico_si_no_existe(self):
        """Si una variante no tiene fila de inventario, se crea automáticamente con stock 0."""
        variante_sin_inventario = Variante.objects.create(
            id_producto=self.producto, nombre='Variante Nueva', creado_por=self.usuario,
        )
        self.assertFalse(
            Inventario.objects.filter(id_variante=variante_sin_inventario).exists()
        )
        movimiento = inv_service.registrar_movimiento(
            self.tipo_entrada,
            '2026-11-22 16:00:00',
            'Entrada variante nueva',
            [{'variante': variante_sin_inventario, 'cantidad': Decimal('50')}],
            self.usuario,
        )
        inventario = Inventario.objects.get(id_variante=variante_sin_inventario)
        self.assertEqual(inventario.stock_actual, Decimal('50'))
        self.assertEqual(movimiento.id_movimiento_inventario, MovimientoInventario.objects.first().id_movimiento_inventario)

    def test_detalles_se_crean_asociados_al_movimiento(self):
        """Cada detalle del movimiento queda vinculado al movimiento creado."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        movimiento = inv_service.registrar_movimiento(
            self.tipo_entrada,
            '2026-11-22 17:00:00',
            'Con detalles',
            [{'variante': self.variante, 'cantidad': Decimal('4')}],
            self.usuario,
        )
        detalle = DetalleMovimiento.objects.get(id_movimiento_inventario=movimiento)
        self.assertEqual(detalle.id_variante, self.variante)
        self.assertEqual(detalle.cantidad, Decimal('4'))

    def test_variante_repetida_se_agrupa_en_un_detalle(self):
        """Si una variante se repite en varios detalles, se agrupan sus cantidades en una sola línea."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        movimiento = inv_service.registrar_movimiento(
            self.tipo_entrada,
            '2026-11-22 17:00:00',
            'Variante repetida',
            [
                {'variante': self.variante, 'cantidad': Decimal('3')},
                {'variante': self.variante, 'cantidad': Decimal('7')},
            ],
            self.usuario,
        )
        detalles = DetalleMovimiento.objects.filter(id_movimiento_inventario=movimiento)
        self.assertEqual(detalles.count(), 1)
        self.assertEqual(detalles.get().cantidad, Decimal('10'))
        inventario = Inventario.objects.get(id_variante=self.variante)
        self.assertEqual(inventario.stock_actual, Decimal('20'))

    def test_rollback_por_fallo_en_segundo_detalle(self):
        """Si falla el segundo detalle de un movimiento, nada se guarda (rollback atómico)."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        stock_antes = Inventario.objects.get(id_variante=self.variante).stock_actual
        movimientos_antes = MovimientoInventario.objects.count()
        detalles_antes = DetalleMovimiento.objects.count()

        with self.assertRaises(ValueError):
            inv_service.registrar_movimiento(
                self.tipo_salida,
                '2026-11-22 18:00:00',
                'Falla a la mitad',
                [
                    {'variante': self.variante, 'cantidad': Decimal('2')},  # válido
                    {'variante': self.variante, 'cantidad': Decimal('999')},  # inválido
                ],
                self.usuario,
            )

        # Rollback completo
        stock_despues = Inventario.objects.get(id_variante=self.variante).stock_actual
        movimientos_despues = MovimientoInventario.objects.count()
        detalles_despues = DetalleMovimiento.objects.count()
        self.assertEqual(stock_antes, stock_despues)
        self.assertEqual(movimientos_antes, movimientos_despues)
        self.assertEqual(detalles_antes, detalles_despues)

    def test_select_for_update_bloquea_fila(self):
        """select_for_update bloquea la fila de inventario dentro de la transacción."""
        inv_service.crear_inventario(self.variante, Decimal('100'), Decimal('10'), self.usuario)
        with transaction.atomic():
            inventario_bloqueado = Inventario.objects.select_for_update().get(id_variante=self.variante)
            self.assertEqual(inventario_bloqueado.stock_actual, Decimal('100'))
            # El bloqueo se libera al salir del bloque atómico

    # --- Casos de error ---

    def test_movimiento_sin_detalles_rechaza(self):
        """Un movimiento sin detalles debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            inv_service.registrar_movimiento(
                self.tipo_entrada,
                '2026-11-22 10:00:00',
                'Sin detalles',
                [],
                self.usuario,
            )

    def test_cantidad_negativa_rechaza(self):
        """Una cantidad negativa en un detalle debe lanzar ValueError."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        with self.assertRaises(ValueError):
            inv_service.registrar_movimiento(
                self.tipo_entrada,
                '2026-11-22 10:00:00',
                'Cantidad negativa',
                [{'variante': self.variante, 'cantidad': Decimal('-5')}],
                self.usuario,
            )

    def test_tipo_movimiento_inexistente_rechaza(self):
        """Un tipo de movimiento que no existe debe lanzar ValueError."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        with self.assertRaises(ValueError):
            inv_service.registrar_movimiento(
                'tipo_inexistente',
                '2026-11-22 10:00:00',
                'Tipo malo',
                [{'variante': self.variante, 'cantidad': Decimal('1')}],
                self.usuario,
            )

    def test_compra_inexistente_rechaza(self):
        """Un id_compra que no existe debe lanzar ValueError."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        with self.assertRaises(ValueError):
            inv_service.registrar_movimiento(
                self.tipo_entrada,
                '2026-11-22 10:00:00',
                'Compra inexistente',
                [{'variante': self.variante, 'cantidad': Decimal('1')}],
                self.usuario,
                id_compra=99999,
            )

    def test_venta_inexistente_rechaza(self):
        """Un id_venta que no existe debe lanzar ValueError."""
        inv_service.crear_inventario(self.variante, Decimal('10'), Decimal('5'), self.usuario)
        with self.assertRaises(ValueError):
            inv_service.registrar_movimiento(
                self.tipo_entrada,
                '2026-11-22 10:00:00',
                'Venta inexistente',
                [{'variante': self.variante, 'cantidad': Decimal('1')}],
                self.usuario,
                id_venta=99999,
            )

    def test_editar_inventario_sin_actualizado_por_rechaza(self):
        """Editar inventario sin actualizado_por debe lanzar ValueError."""
        inventario = inv_service.crear_inventario(
            self.variante, Decimal('10'), Decimal('5'), self.usuario,
        )
        with self.assertRaises(ValueError):
            inv_service.editar_inventario(
                inventario,
                stock_actual=Decimal('20'),
                actualizado_por=None,
            )
