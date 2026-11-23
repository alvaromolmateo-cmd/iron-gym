from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from .forms import MyUserCreationForm
from .models import MyUser


# UD5.1 - Pruebas del usuario personalizado.
class UsuarioTests(TestCase):
    def test_crear_usuario_sin_username(self):
        user = MyUser.objects.create_user('ana@EXAMPLE.COM', password='UnaClaveDePrueba-2026!')
        self.assertEqual(user.email, 'ana@example.com')
        self.assertIsNone(user.username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password('UnaClaveDePrueba-2026!'))
        self.assertNotEqual(user.password, 'UnaClaveDePrueba-2026!')
        self.assertEqual(authenticate(username=user.email, password='UnaClaveDePrueba-2026!'), user)

    def test_email_obligatorio(self):
        with self.assertRaises(ValueError):
            MyUser.objects.create_user('')

    def test_usuario_inactivo_no_accede(self):
        user = MyUser.objects.create_user('inactivo@example.com', password='UnaClaveDePrueba-2026!', is_active=False)
        self.assertIsNone(authenticate(username=user.email, password='UnaClaveDePrueba-2026!'))

    def test_superusuario_y_administrador(self):
        user = MyUser.objects.create_superuser('admin@example.com', password='UnaClaveDePrueba-2026!')
        self.assertTrue(user.is_superuser and user.is_staff and user.is_active)
        self.assertTrue(self.client.login(username=user.email, password='UnaClaveDePrueba-2026!'))
        for name, args in [('admin:usuarios_myuser_changelist', []),
                           ('admin:usuarios_myuser_add', []),
                           ('admin:usuarios_myuser_change', [user.pk])]:
            self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200)

    def test_admin_cifra_password_y_rechaza_email_repetido(self):
        datos = {'email': 'nuevo@example.com', 'password1': 'UnaClaveDePrueba-2026!',
                 'password2': 'UnaClaveDePrueba-2026!'}
        form = MyUserCreationForm(data=datos)
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertTrue(user.check_password(datos['password1']))
        repetido = MyUserCreationForm(data=datos)
        self.assertFalse(repetido.is_valid())
        self.assertIn('email', repetido.errors)

    def test_passwords_distintas(self):
        form = MyUserCreationForm(data={'email': 'nuevo@example.com', 'password1': 'abc', 'password2': 'xyz'})
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
