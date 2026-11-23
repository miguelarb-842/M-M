"""Pruebas de grupos y permisos: los 4 grupos existen con los permisos correctos."""
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.MyM.models import (
    TipoMovimiento, EstadoCompra, CompaniaTelefonica,
    Venta, DetalleVenta, Compra, DetalleCompra, Distribuidor,
    Producto, Variante, Marca, Categoria, Inventario, MovimientoInventario,
)


class GruposTest(TestCase):
    def test_grupos_creados(self):
        """Los 4 grupos deben existir en la base de datos."""
        nombres_esperados = [
            'gestor_de_ventas',
            'gestor_de_compras',
            'gestor_de_productos',
            'gestor_de_inventario',
        ]
        for nombre in nombres_esperados:
            self.assertTrue(
                Group.objects.filter(name=nombre).exists(),
                f'El grupo {nombre} no existe',
            )

    def test_gestor_de_ventas_permisos(self):
        """gestor_de_ventas tiene add/change/delete/view sobre venta y detalleventa."""
        grupo = Group.objects.get(name='gestor_de_ventas')
        codenames = sorted(p.codename for p in grupo.permissions.all())
        esperados = sorted([
            'add_venta', 'change_venta', 'delete_venta', 'view_venta',
            'add_detalleventa', 'change_detalleventa', 'delete_detalleventa', 'view_detalleventa',
        ])
        self.assertEqual(codenames, esperados)

    def test_gestor_de_compras_permisos(self):
        """gestor_de_compras tiene CRUD sobre compra, detallecompra, distribuidor, estadocompra."""
        grupo = Group.objects.get(name='gestor_de_compras')
        codenames = sorted(p.codename for p in grupo.permissions.all())
        esperados = sorted([
            'add_compra', 'change_compra', 'delete_compra', 'view_compra',
            'add_detallecompra', 'change_detallecompra', 'delete_detallecompra', 'view_detallecompra',
            'add_distribuidor', 'change_distribuidor', 'delete_distribuidor', 'view_distribuidor',
            'add_estadocompra', 'change_estadocompra', 'delete_estadocompra', 'view_estadocompra',
        ])
        self.assertEqual(codenames, esperados)

    def test_gestor_de_productos_permisos(self):
        """gestor_de_productos tiene CRUD sobre producto, variante, marca, categoria."""
        grupo = Group.objects.get(name='gestor_de_productos')
        codenames = sorted(p.codename for p in grupo.permissions.all())
        esperados = sorted([
            'add_producto', 'change_producto', 'delete_producto', 'view_producto',
            'add_variante', 'change_variante', 'delete_variante', 'view_variante',
            'add_marca', 'change_marca', 'delete_marca', 'view_marca',
            'add_categoria', 'change_categoria', 'delete_categoria', 'view_categoria',
        ])
        self.assertEqual(codenames, esperados)

    def test_gestor_de_inventario_permisos(self):
        """gestor_de_inventario tiene CRUD sobre inventario, movimiento, tipo_movimiento y solo view sobre compra, venta."""
        grupo = Group.objects.get(name='gestor_de_inventario')
        codenames = sorted(p.codename for p in grupo.permissions.all())
        esperados = sorted([
            'add_inventario', 'change_inventario', 'delete_inventario', 'view_inventario',
            'add_movimientoinventario', 'change_movimientoinventario', 'delete_movimientoinventario', 'view_movimientoinventario',
            'add_tipomovimiento', 'change_tipomovimiento', 'delete_tipomovimiento', 'view_tipomovimiento',
            'view_compra', 'view_venta',
        ])
        self.assertEqual(codenames, esperados)
        # No debe tener permisos de escritura sobre compra/venta
        self.assertNotIn('add_compra', codenames)
        self.assertNotIn('add_venta', codenames)


class DatosBaseTest(TestCase):
    def test_tipos_movimiento_creados(self):
        """Los 4 tipos de movimiento existen."""
        nombres = ['entrada', 'salida', 'ajuste positivo', 'ajuste negativo']
        for nombre in nombres:
            self.assertTrue(
                TipoMovimiento.objects.filter(nombre=nombre).exists(),
                f'Tipo de movimiento {nombre} no existe',
            )

    def test_estados_compra_creados(self):
        """Los 3 estados de compra existen."""
        nombres = ['entregada', 'pendiente', 'cancelada']
        for nombre in nombres:
            self.assertTrue(
                EstadoCompra.objects.filter(nombre=nombre).exists(),
                f'Estado de compra {nombre} no existe',
            )

    def test_companias_telefonicas_creadas(self):
        """Las 2 compañías telefónicas existen."""
        nombres = ['tigo', 'claro']
        for nombre in nombres:
            self.assertTrue(
                CompaniaTelefonica.objects.filter(nombre=nombre).exists(),
                f'Compañía telefónica {nombre} no existe',
            )
