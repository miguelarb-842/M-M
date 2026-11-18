from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError
from django.test import Client, TestCase

from .models import Usuario


class UsuarioYPermisosTests(TestCase):
    def _perm(self, codename):
        return Permission.objects.get(codename=codename, content_type__app_label='MyM')

    def test_usuario_con_grupo_default(self):
        u = Usuario.objects.create_user('nuevo', 'pass123')
        self.assertEqual(list(u.groups.values_list('name', flat=True)), ['general'])

    def test_clave_se_guarda_hasheada(self):
        u = Usuario.objects.create_user('nuevo', 'pass123')
        self.assertTrue(u.password.startswith(('pbkdf2_', 'argon2', 'scrypt')))
        self.assertNotEqual(u.password, 'pass123')

    def test_authenticate(self):
        Usuario.objects.create_user('nuevo', 'pass123')
        self.assertIsNotNone(authenticate(nombre='nuevo', password='pass123'))
        self.assertIsNone(authenticate(nombre='nuevo', password='mala'))

    def test_permisos_por_grupo(self):
        vendedor = Group.objects.create(name='vendedor')
        vendedor.permissions.add(self._perm('add_compra'))
        u = Usuario.objects.create_user('vendedor1', 'pass123', groups=[vendedor])
        otro = Usuario.objects.create_user('otro', 'pass123')
        superu = Usuario.objects.create_superuser('admin', 'pass123')

        self.assertTrue(u.has_perm('MyM.add_compra'))
        self.assertFalse(u.has_perm('MyM.view_compra'))
        self.assertFalse(otro.has_perm('MyM.add_compra'))
        self.assertTrue(superu.has_perm('MyM.view_compra'))
        self.assertTrue(superu.has_perm('MyM.add_producto'))

    def test_fechas_automaticas(self):
        u = Usuario.objects.create_user('nuevo', 'pass123')
        self.assertIsNotNone(u.fecha_creacion)
        self.assertIsNone(u.fecha_actualizacion)
        # actualizar exige identificar quién actualiza (CHECK de auditoría)
        with self.assertRaises(ValueError):
            u.save()
        u.actualizado_por = u
        u.save()
        self.assertIsNotNone(u.fecha_actualizacion)

    def test_check_auditoria_en_db(self):
        # CHECK: fecha_actualizacion y actualizado_por deben ir juntos
        with self.assertRaises(IntegrityError):
            Usuario.objects.create_user('malo', 'pass123', fecha_actualizacion='2026-01-01')

    def test_primer_usuario_sin_creador(self):
        u = Usuario.objects.create_user('primero', 'pass123')
        self.assertIsNone(u.creado_por)

    def test_admin_accesible(self):
        superu = Usuario.objects.create_superuser('admin', 'pass123')
        c = Client()
        c.force_login(superu)
        self.assertEqual(c.get('/admin/').status_code, 200)
        self.assertEqual(c.get('/admin/MyM/usuario/').status_code, 200)
        self.assertEqual(c.get('/admin/MyM/marca/').status_code, 200)
        self.assertEqual(c.get('/admin/auth/group/').status_code, 200)
