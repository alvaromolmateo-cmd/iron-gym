# UD3.1 / UD3.6 / UD3.7 / UD3.8 - Comprobaciones en una BD temporal.
from datetime import time, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from billing.models import Cliente, Factura, Cobro
from core.models import Perfil, Instalacion, Horario, Reserva, Bloqueo
from common import actividadorm as orm


class PaginasTests(TestCase):
    def test_listas_vacias_y_paginas_comunes(self):
        for nombre in ("home", "panel"):
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200)
        for nombre in ("cliente", "factura", "cobro", "perfil", "instalacion", "horario", "reserva", "bloqueo"):
            with self.subTest(modelo=nombre):
                response = self.client.get(reverse(nombre + "_list"))
                self.assertContains(response, "No hay")
                self.assertEqual(self.client.get(reverse(nombre + "_detail", args=[999])).status_code, 404)

    def test_detalles_y_paginacion_de_todos_los_modelos(self):
        hoy = timezone.localdate()
        ahora = timezone.now()
        for i in range(11):
            usuario = User.objects.create_user(username=f"socio{i}")
            cliente = Cliente.objects.create(nombre=f"Cliente{i}", apellidos="Prueba", nif=f"N{i}", email=f"c{i}@example.com")
            factura = Factura.objects.create(cliente=cliente, numero=f"F{i:02}", concepto="Cuota")
            cobro = Cobro.objects.create(factura=factura, importe=5)
            perfil = Perfil.objects.create(usuario=usuario, dni=f"D{i}")
            instalacion = Instalacion.objects.create(nombre=f"Pista{i:02}")
            horario = Horario.objects.create(instalacion=instalacion, dia_semana=0, hora_apertura=time(9), hora_cierre=time(21))
            reserva = Reserva.objects.create(usuario=usuario, instalacion=instalacion, fecha=hoy, hora_inicio=time(10), hora_fin=time(11))
            bloqueo = Bloqueo.objects.create(instalacion=instalacion, inicio=ahora, fin=ahora + timedelta(hours=1), motivo="Limpieza")
        objetos = dict(cliente=cliente, factura=factura, cobro=cobro, perfil=perfil, instalacion=instalacion, horario=horario, reserva=reserva, bloqueo=bloqueo)
        for nombre, objeto in objetos.items():
            with self.subTest(modelo=nombre):
                url = reverse(nombre + "_list")
                primera = self.client.get(url)
                segunda = self.client.get(url, {"page": 2})
                self.assertEqual(len(primera.context["object_list"]), 10)
                self.assertEqual(len(segunda.context["object_list"]), 1)
                self.assertContains(primera, "?page=2")
                self.assertContains(segunda, "Anterior")
                self.assertEqual(self.client.get(url, {"page": 3}).status_code, 404)
                detalle = self.client.get(reverse(nombre + "_detail", args=[objeto.pk]))
                self.assertEqual(detalle.status_code, 200)
        self.assertContains(self.client.get(reverse("cobro_detail", args=[cobro.pk])), str(cliente))
        self.assertContains(self.client.get(reverse("perfil_detail", args=[perfil.pk])), "Socio")


class ORMTests(TestCase):
    def setUp(self):
        self.ana = Cliente.objects.create(id=1, nombre="Ana", apellidos="Pérez González", nif="92436593F", email="ana@example.com")
        self.manu = Cliente.objects.create(id=2, nombre="Manuel", apellidos="Otros", nif="74111", email="manu@example.com")
        self.pablo = Cliente.objects.create(id=3, nombre="Pablo", apellidos="Otros", nif="80111", email="pablo@example.com")
        self.f1 = Factura.objects.create(id=1, cliente=self.ana, numero="F01", concepto="PHP python", total=0)
        self.f2 = Factura.objects.create(id=2, cliente=self.ana, numero="F02", concepto="PHP", total=5)
        self.f3 = Factura.objects.create(id=3, cliente=self.manu, numero="F06", concepto="Cuota", total=10)
        self.f4 = Factura.objects.create(id=4, cliente=self.pablo, numero="F060", concepto="Cuota", total=20)
        self.c1 = Cobro.objects.create(id=2, factura=self.f1, importe=5)
        self.c2 = Cobro.objects.create(id=3, factura=self.f2, importe=10)
        self.c3 = Cobro.objects.create(id=4, factura=self.f3, importe=11)
        self.c4 = Cobro.objects.create(id=5, factura=self.f4, importe=1)

    def test_consultas_1_a_13(self):
        casos = [
            (orm.get_clientes_all, [1, 2, 3]),
            (orm.get_factura_first_3, [1, 2, 3]),
            (orm.get_factura_0, [1]),
            (orm.get_cliente_not_0612, [1, 3]),
            (orm.get_cliente_dni_apellido, [1]),
            (orm.get_cli_id_lt_2_num_fact_des, [1]),
            (orm.get_cli_id_gt_2, [3]),
            (orm.get_fact_des_nom_des, [1, 2]),
            (orm.get_fact_not_1, [2, 3, 4]),
            (orm.get_cobro_fact6_not_manu, [5]),
            (orm.get_fact_gt_5, [2, 3, 4]),
            (orm.get_cobro_5_10, [2, 3]),
        ]
        for funcion, ids in casos:
            with self.subTest(operacion=funcion.__name__):
                self.assertCountEqual(funcion().values_list("pk", flat=True), ids)
        self.assertEqual(list(orm.get_fact_des_nom_des()), [self.f1, self.f2])
        self.assertEqual(orm.get_cobro_python_id2(), self.c1)

    def test_creacion_y_ultima_factura(self):
        cliente = orm.create_cliente()
        factura = orm.create_factura()
        self.assertEqual(factura.cliente, cliente)
        self.assertEqual(factura.fecha, timezone.localdate() - timedelta(days=1))
        self.assertEqual(factura.total, Decimal("100.00"))
        self.assertEqual(orm.update_last_factura().pk, factura.pk)
        factura.refresh_from_db()
        self.assertTrue(factura.concepto.endswith("(última)"))

    def test_actualizaciones_y_borrados_selectivos(self):
        self.assertEqual(orm.update_cobro_fact2_x2(), 1)
        self.c2.refresh_from_db()
        self.assertEqual(self.c2.importe, Decimal("20.00"))
        self.assertEqual(orm.update_cobro_fact1_cligonz_div2(), 1)
        self.c1.refresh_from_db()
        self.assertEqual(self.c1.importe, Decimal("2.50"))
        orm.delete_cobro_fact_lt_1()
        self.assertFalse(Cobro.objects.filter(pk=self.c1.pk).exists())
        orm.delete_cobro_cli_pablo()
        self.assertCountEqual(Cobro.objects.values_list("pk", flat=True), [self.c2.pk, self.c3.pk])
        self.assertEqual(Factura.objects.count(), 4)

    def test_operaciones_sin_resultados(self):
        Cobro.objects.all().delete()
        Factura.objects.all().delete()
        self.assertIsNone(orm.get_cobro_python_id2())
        self.assertIsNone(orm.update_last_factura())
