from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from .forms import MyUserCreationForm
from .models import MyUser


# UD5.3 - Todas las operaciones privadas requieren sesión, también los POST.
class ProteccionVistasTests(TestCase):
    def test_todas_las_vistas_privadas_redirigen_sin_sesion(self):
        urls = [reverse('panel')]
        for modelo in ('cliente', 'factura', 'cobro', 'perfil', 'instalacion', 'horario', 'reserva', 'bloqueo'):
            for accion in ('list', 'create', 'detail', 'update', 'delete'):
                args = [999] if accion in ('detail', 'update', 'delete') else []
                urls.append(reverse(modelo + '_' + accion, args=args))
        for url in urls:
            for metodo in ('get', 'post'):
                with self.subTest(url=url, metodo=metodo):
                    respuesta = getattr(self.client, metodo)(url)
                    self.assertRedirects(respuesta, reverse(settings.LOGIN_URL) + '?next=' + url)

    def test_inicio_y_login_siguen_publicos(self):
        for nombre in ('home', 'login'):
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200)

    def test_acceso_tras_login_y_proteccion_tras_logout(self):
        usuario = MyUser.objects.create_user('privado@example.com', password='ClaveDeEnsayo-2026!')
        destino = reverse('instalacion_list') + '?ordering=desc'
        respuesta = self.client.get(destino)
        login = self.client.get(respuesta.url)
        self.assertContains(login, 'name="next"')
        respuesta = self.client.post(reverse('login'), {
            'username': usuario.email, 'password': 'ClaveDeEnsayo-2026!', 'next': destino,
        })
        self.assertRedirects(respuesta, destino)
        self.client.post(reverse('logout'))
        self.assertEqual(self.client.get(destino).status_code, 302)


# UD5.2 - Acceso, persistencia de sesión, errores y cierre seguro.
class LoginLogoutTests(TestCase):
    def setUp(self):
        self.password = 'ClaveDeEnsayo-2026!'
        self.user = MyUser.objects.create_user('socio@example.com', password=self.password)

    def test_login_email_y_sesion(self):
        self.assertContains(self.client.get(reverse('login')), 'type="email"')
        respuesta = self.client.post(reverse('login'), {'username': self.user.email, 'password': self.password})
        self.assertRedirects(respuesta, reverse('panel'))
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))
        self.assertContains(self.client.get(reverse('home')), self.user.email)

    def test_password_incorrecta_o_usuario_inactivo(self):
        respuesta = self.client.post(reverse('login'), {'username': self.user.email, 'password': 'incorrecta'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.context['form'].non_field_errors())
        self.assertNotIn('_auth_user_id', self.client.session)
        self.user.is_active = False
        self.user.save()
        self.client.post(reverse('login'), {'username': self.user.email, 'password': self.password})
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_next_local_y_rechazo_de_redireccion_externa(self):
        for destino, esperado in [('/instalacion_list/', '/instalacion_list/'),
                                  ('https://example.com/externo', reverse('panel'))]:
            self.client.logout()
            respuesta = self.client.post(reverse('login'), {
                'username': self.user.email, 'password': self.password, 'next': destino,
            })
            self.assertRedirects(respuesta, esperado)

    def test_logout_post_y_csrf(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.get(reverse('logout')).status_code, 405)
        self.assertEqual(client.post(reverse('logout')).status_code, 403)
        client.get(reverse('home'))
        token = client.cookies['csrftoken'].value
        respuesta = client.post(reverse('logout'), {'csrfmiddlewaretoken': token})
        self.assertRedirects(respuesta, reverse('home'))
        self.assertNotIn('_auth_user_id', client.session)


# UD5.1 - Comprobar el manager, autenticación por email y administrador.
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
