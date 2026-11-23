"""Smoke tests: verificación básica de que la aplicación carga y responde."""
from django.test import TestCase, Client, override_settings
from django.urls import reverse


class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_login_url_responde(self):
        """La URL de login debe devolver 200 (GET) sin errores."""
        response = self.client.get(reverse('MyM:login'))
        self.assertEqual(response.status_code, 200)

    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_logout_redirige_a_login(self):
        """El logout sin sesión debe redirigir al login."""
        response = self.client.get(reverse('MyM:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('MyM:login'))

    def test_urls_nombre_correcto(self):
        """Los names de las URLs están definidos."""
        urls = ['MyM:login', 'MyM:logout', 'MyM:inicio']
        for url_name in urls:
            try:
                reverse(url_name)
            except Exception as exc:
                self.fail(f'URL {url_name} no se puede resolver: {exc}')
