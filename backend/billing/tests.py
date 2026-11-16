from django.test import TestCase
from django.urls import reverse
from .models import Cliente, Factura, Cobro
from .forms import FacturaForm, CobroForm


# UD4.1 / UD4.2b-g - Comprobaciones con una base de datos de pruebas aislada.
class VistasEdicionTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Ana', apellidos='Prueba', nif='PRUEBA', email='ana@example.com',
        )
        self.factura = Factura.objects.create(cliente=self.cliente, numero='TEST-1', total=100)

    def test_formularios_de_creacion_y_contexto(self):
        for modelo in ['cliente', 'factura', 'cobro', 'perfil', 'instalacion', 'horario', 'reserva', 'bloqueo']:
            with self.subTest(modelo=modelo):
                respuesta = self.client.get(reverse(modelo + '_create'))
                self.assertEqual(respuesta.status_code, 200)
                self.assertTemplateUsed(respuesta, 'base_create_update.html')
                self.assertContains(respuesta, 'Crear ' + modelo)
                self.assertIsNone(respuesta.context['url_borrado'])
                self.assertNotContains(respuesta, '>Eliminar</a>')

    def test_crear_y_actualizar_cliente(self):
        datos = {'nombre': 'Luis', 'apellidos': 'Prueba', 'nif': 'OTRO', 'email': 'luis@example.com'}
        respuesta = self.client.post(reverse('cliente_create'), datos)
        cliente = Cliente.objects.get(nif='OTRO')
        destino = reverse('cliente_update', args=[cliente.pk])
        self.assertRedirects(respuesta, destino)
        respuesta = self.client.get(destino)
        self.assertContains(respuesta, reverse('cliente_delete', args=[cliente.pk]))
        datos['nombre'] = 'Luis actualizado'
        self.assertRedirects(self.client.post(destino, datos), destino)
        cliente.refresh_from_db()
        self.assertEqual(cliente.nombre, 'Luis actualizado')

    def test_cobro_limite_y_exceso(self):
        datos = {'factura': self.factura.pk, 'fecha': '2026-11-16', 'importe': '100'}
        respuesta = self.client.post(reverse('cobro_create'), datos)
        cobro = Cobro.objects.get()
        self.assertRedirects(respuesta, reverse('cobro_update', args=[cobro.pk]))
        datos['importe'] = '0.01'
        respuesta = self.client.post(reverse('cobro_create'), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'La suma de los cobros no puede superar')
        self.assertContains(respuesta, 'alert-danger')
        self.assertEqual(Cobro.objects.count(), 1)

    def test_actualizar_cobro_no_duplica_importe_y_rechaza_exceso(self):
        cobro = Cobro.objects.create(factura=self.factura, importe=60)
        Cobro.objects.create(factura=self.factura, importe=40)
        destino = reverse('cobro_update', args=[cobro.pk])
        datos = {'factura': self.factura.pk, 'fecha': '2026-11-16', 'importe': '60'}
        self.assertRedirects(self.client.post(destino, datos), destino)
        datos['importe'] = '61'
        respuesta = self.client.post(destino, datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'La suma de los cobros no puede superar')
        cobro.refresh_from_db()
        self.assertEqual(cobro.importe, 60)

    def test_cambio_de_factura_comprueba_la_factura_destino(self):
        otra = Factura.objects.create(cliente=self.cliente, numero='TEST-2', total=20)
        cobro = Cobro.objects.create(factura=self.factura, importe=30)
        respuesta = self.client.post(reverse('cobro_update', args=[cobro.pk]), {
            'factura': otra.pk, 'fecha': '2026-11-16', 'importe': '30',
        })
        self.assertEqual(respuesta.status_code, 200)
        cobro.refresh_from_db()
        self.assertEqual(cobro.factura_id, self.factura.pk)

    def test_borrado_protegido_informa_sin_eliminar(self):
        respuesta = self.client.post(reverse('cliente_delete', args=[self.cliente.pk]), follow=True)
        self.assertRedirects(respuesta, reverse('cliente_list'))
        self.assertContains(respuesta, 'Existen dependencias para el objeto ' + str(self.cliente))
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())
        cobro = Cobro.objects.create(factura=self.factura, importe=10)
        respuesta = self.client.post(reverse('factura_delete', args=[self.factura.pk]), follow=True)
        self.assertContains(respuesta, 'Existen dependencias para el objeto ' + str(self.factura))
        self.assertTrue(Cobro.objects.filter(pk=cobro.pk).exists())

    def test_borrado_requiere_post_y_funciona_sin_dependencias(self):
        destino = reverse('factura_delete', args=[self.factura.pk])
        respuesta = self.client.get(destino)
        self.assertTemplateUsed(respuesta, 'base_confirm_delete.html')
        self.assertTrue(Factura.objects.filter(pk=self.factura.pk).exists())
        self.assertRedirects(self.client.post(destino), reverse('factura_list'))
        self.assertFalse(Factura.objects.filter(pk=self.factura.pk).exists())

    # UD4.3b - Cero y negativos se rechazan; los importes positivos se admiten.
    def test_validacion_de_importes_en_formularios(self):
        for importe in ['0', '-1', '0.01']:
            factura = FacturaForm(data={
                'cliente': self.cliente.pk, 'numero': 'NUEVA', 'concepto': 'Prueba',
                'fecha': '2026-11-16', 'total': importe,
            })
            cobro = CobroForm(data={
                'factura': self.factura.pk, 'fecha': '2026-11-16', 'importe': importe,
            })
            for formulario, campo in [(factura, 'total'), (cobro, 'importe')]:
                with self.subTest(importe=importe, campo=campo):
                    self.assertEqual(formulario.is_valid(), importe == '0.01')
                    if importe != '0.01':
                        self.assertIn(campo, formulario.errors)

    # UD4.4a-b - Mensaje del objeto y un solo formulario con protección CSRF.
    def test_mensajes_de_exito_y_formulario_crispy(self):
        datos = {'nombre': 'Eva', 'apellidos': 'Prueba', 'nif': 'EVA', 'email': 'eva@example.com'}
        respuesta = self.client.post(reverse('cliente_create'), datos, follow=True)
        cliente = Cliente.objects.get(nif='EVA')
        self.assertContains(respuesta, '{} creado correctamente.'.format(cliente))
        self.assertContains(respuesta, '<form ', count=1)
        self.assertContains(respuesta, 'name="csrfmiddlewaretoken"', count=1)
        self.assertContains(respuesta, 'novalidate')
        self.assertContains(respuesta, 'col-3')
        self.assertContains(respuesta, 'col-6')
        datos['nombre'] = 'Eva actualizada'
        respuesta = self.client.post(reverse('cliente_update', args=[cliente.pk]), datos, follow=True)
        cliente.refresh_from_db()
        self.assertContains(respuesta, '{} actualizado correctamente.'.format(cliente))
