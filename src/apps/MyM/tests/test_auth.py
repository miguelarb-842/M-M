"""Pruebas de autenticación: login por nombre de usuario, logout y contraseñas."""
from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse


class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.usuario = self.User.objects.create_user(
            nombre='juanperez',
            password='ClaveSegura123',
            correo_electronico='juan@ejemplo.com',
        )

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_login_por_nombre_exitoso(self):
        """Autenticación con nombre de usuario y contraseña correcta."""
        response = self.client.post(
            reverse('MyM:login'),
            {'username': 'juanperez', 'password': 'ClaveSegura123'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('MyM:inicio'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_login_por_correo_falla(self):
        """No se permite autenticar con correo electrónico (solo nombre)."""
        response = self.client.post(
            reverse('MyM:login'),
            {'username': 'juan@ejemplo.com', 'password': 'ClaveSegura123'},
        )
        # Debe devolver 200 (se queda en login con error) y no autenticar
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_login_contrasena_incorrecta(self):
        """Contraseña incorrecta debe fallar y no autenticar."""
        response = self.client.post(
            reverse('MyM:login'),
            {'username': 'juanperez', 'password': 'ClaveMal123'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_login_usuario_inexistente(self):
        """Usuario que no existe debe fallar."""
        response = self.client.post(
            reverse('MyM:login'),
            {'username': 'noexiste', 'password': 'ClaveSegura123'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_logout_exitoso(self):
        """Logout después de login debe redirigir al login y desautenticar."""
        self.client.post(
            reverse('MyM:login'),
            {'username': 'juanperez', 'password': 'ClaveSegura123'},
        )
        response = self.client.get(reverse('MyM:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('MyM:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
