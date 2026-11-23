import re
from urllib.parse import urlsplit
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import MyUser


# UD5.4 - Probar la versión Allauth sin enviar correos reales.
@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AllauthTests(TestCase):
    def setUp(self):
        self.password = 'ClaveDeEnsayo-2026!'
        self.user = MyUser.objects.create_user('allauth@example.com', password=self.password)

    def test_plantilla_incluida_y_enlace_recuperacion(self):
        respuesta = self.client.get(reverse('account_login'))
        self.assertTemplateUsed(respuesta, 'account/login.html')
        self.assertContains(respuesta, reverse('account_reset_password'))

    def test_acceso_y_logout(self):
        respuesta = self.client.post(reverse('account_login'), {'login': self.user.email, 'password': self.password})
        self.assertRedirects(respuesta, reverse('panel'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))
        self.assertRedirects(self.client.post(reverse('account_logout')), reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_password_incorrecta_no_inicia_sesion(self):
        respuesta = self.client.post(reverse('account_login'), {'login': self.user.email, 'password': 'incorrecta'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.context['form'].errors)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_recuperacion_completa_con_correo_en_memoria(self):
        respuesta = self.client.post(reverse('account_reset_password'), {'email': self.user.email})
        self.assertRedirects(respuesta, reverse('account_reset_password_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        enlace = re.search(r'https?://[^\s]+/accounts/password/reset/key/[^\s]+', mail.outbox[0].body).group(0)
        respuesta = self.client.get(urlsplit(enlace).path, follow=True)
        self.assertEqual(respuesta.status_code, 200)
        destino = respuesta.request['PATH_INFO']
        nueva = 'OtraClaveSegura-2026!'
        respuesta = self.client.post(destino, {'password1': nueva, 'password2': nueva})
        self.assertEqual(respuesta.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(nueva))
        self.assertFalse(self.user.check_password(self.password))
