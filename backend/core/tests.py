from django.test import TestCase
from django.urls import reverse
from .models import TipoInstalacion, Instalacion, DiaSemana, Horario, Bloqueo
from django.contrib.auth.models import User
from .models import TipoPerfil, EstadoReserva
from .forms import PerfilForm, InstalacionForm, ReservaForm


# UD4.1 / UD4.2h - Las validaciones deben actuar al crear y al actualizar.
class IntervalosTests(TestCase):
    def setUp(self):
        tipo = TipoInstalacion.objects.create(codigo='prueba', nombre='Prueba')
        self.instalacion = Instalacion.objects.create(nombre='Sala de prueba', tipo=tipo)
        self.dia, _ = DiaSemana.objects.get_or_create(numero=1, defaults={'nombre': 'Lunes'})

    def test_horario_creacion_y_actualizacion(self):
        datos = {'instalacion': self.instalacion.pk, 'dia_semana': self.dia.pk,
                 'hora_apertura': '09:00', 'hora_cierre': '08:00', 'duracion_franja': 60}
        for cierre in ['08:00', '09:00']:
            datos['hora_cierre'] = cierre
            respuesta = self.client.post(reverse('horario_create'), datos)
            self.assertContains(respuesta, 'La hora de cierre debe ser posterior')
            self.assertEqual(Horario.objects.count(), 0)
        datos['hora_cierre'] = '10:00'
        respuesta = self.client.post(reverse('horario_create'), datos)
        horario = Horario.objects.get()
        destino = reverse('horario_update', args=[horario.pk])
        self.assertRedirects(respuesta, destino)
        datos['hora_cierre'] = '09:00'
        self.assertContains(self.client.post(destino, datos), 'La hora de cierre debe ser posterior')
        horario.refresh_from_db()
        self.assertEqual(horario.hora_cierre.hour, 10)
        datos['hora_cierre'] = '11:00'
        self.assertRedirects(self.client.post(destino, datos), destino)

    def test_bloqueo_creacion_y_actualizacion(self):
        datos = {'instalacion': self.instalacion.pk, 'inicio': '2026-11-16 09:00',
                 'fin': '2026-11-16 08:00', 'motivo': 'Mantenimiento', 'creado_por': ''}
        for fin in ['2026-11-16 08:00', '2026-11-16 09:00']:
            datos['fin'] = fin
            respuesta = self.client.post(reverse('bloqueo_create'), datos)
            self.assertContains(respuesta, 'El fin del bloqueo debe ser posterior')
            self.assertEqual(Bloqueo.objects.count(), 0)
        datos['fin'] = '2026-11-16 10:00'
        respuesta = self.client.post(reverse('bloqueo_create'), datos)
        bloqueo = Bloqueo.objects.get()
        destino = reverse('bloqueo_update', args=[bloqueo.pk])
        self.assertRedirects(respuesta, destino)
        fin_anterior = bloqueo.fin
        datos['fin'] = '2026-11-16 08:00'
        self.assertContains(self.client.post(destino, datos), 'El fin del bloqueo debe ser posterior')
        bloqueo.refresh_from_db()
        self.assertEqual(bloqueo.fin, fin_anterior)
        datos['fin'] = '2026-11-16 11:00'
        self.assertRedirects(self.client.post(destino, datos), destino)

    # UD4.2i - La URL modifica el orden sin cambiar la ordenación del modelo.
    def test_ordenacion_por_id_y_orden_predeterminado(self):
        otra = Instalacion.objects.create(nombre='A primera por nombre', tipo=self.instalacion.tipo)
        for parametro, esperado in [('asc', [self.instalacion.pk, otra.pk]),
                                    ('desc', [otra.pk, self.instalacion.pk]),
                                    ('otro', [otra.pk, self.instalacion.pk]),
                                    ('', [otra.pk, self.instalacion.pk])]:
            respuesta = self.client.get(reverse('instalacion_list'), {'ordering': parametro})
            self.assertEqual([obj.pk for obj in respuesta.context['object_list']], esperado)


# UD4.1 / UD4.3c - Validaciones de formularios, incluidos campos vacíos.
class FormulariosCoreTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create(username='prueba_formularios')
        self.tipo, _ = TipoPerfil.objects.get_or_create(codigo='socio', defaults={'nombre': 'Socio'})
        self.estado, _ = EstadoReserva.objects.get_or_create(codigo='confirmada', defaults={'nombre': 'Confirmada'})
        self.tipo_instalacion = TipoInstalacion.objects.create(codigo='test', nombre='Tipo de prueba')
        self.instalacion = Instalacion.objects.create(nombre='Sala', tipo=self.tipo_instalacion)

    def test_caducidad_opcional_y_no_anterior_al_alta(self):
        for caducidad, valido in [('', True), ('2026-11-16', True), ('2026-11-17', True), ('2026-11-15', False)]:
            formulario = PerfilForm(data={
                'usuario': self.usuario.pk, 'tipo': self.tipo.pk, 'dni': 'PRUEBA',
                'fecha_alta': '2026-11-16', 'fecha_caducidad': caducidad,
            })
            self.assertEqual(formulario.is_valid(), valido, formulario.errors)
            if not valido:
                self.assertIn('La fecha de caducidad', str(formulario.non_field_errors()))

    def test_capacidad_positiva(self):
        for capacidad, valido in [('0', False), ('-1', False), ('1', True)]:
            formulario = InstalacionForm(data={
                'nombre': 'Otra sala', 'tipo': self.tipo_instalacion.pk, 'capacidad': capacidad,
            })
            self.assertEqual(formulario.is_valid(), valido, formulario.errors)
            if not valido:
                self.assertIn('capacidad', formulario.errors)

    def test_intervalo_reserva(self):
        for fin, valido in [('08:00', False), ('09:00', False), ('10:00', True)]:
            formulario = ReservaForm(data={
                'usuario': self.usuario.pk, 'instalacion': self.instalacion.pk,
                'fecha': '2026-11-16', 'hora_inicio': '09:00', 'hora_fin': fin,
                'estado': self.estado.pk,
            })
            self.assertEqual(formulario.is_valid(), valido, formulario.errors)
            if not valido:
                self.assertIn('La hora de fin', str(formulario.non_field_errors()))

    def test_campos_ausentes_no_provocan_excepcion(self):
        for clase in [PerfilForm, InstalacionForm, ReservaForm]:
            self.assertFalse(clase(data={}).is_valid())
