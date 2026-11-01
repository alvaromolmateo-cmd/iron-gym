"""UD3.6 - Operaciones del anexo IV. Importar desde manage.py shell.

Las funciones 14 a 20 modifican datos: ejecutarlas solo sobre datos de práctica.
Los nombres se conservan aunque alguna descripción del enunciado no coincida.
"""
from datetime import timedelta
from decimal import Decimal
from uuid import uuid4

from django.db.models import F
from django.utils import timezone

from billing.models import Cliente, Factura, Cobro


# UD3.6a - Operación 1
def get_clientes_all():
    return Cliente.objects.all()


# UD3.6b - Operación 2
def get_factura_first_3():
    return Factura.objects.all()[:3]


# UD3.6c - Operación 3: el importe de una factura se llama total.
def get_factura_0():
    return Factura.objects.filter(total=0)


# UD3.6d - Operación 4: la descripción pide excluir el prefijo 74.
def get_cliente_not_0612():
    return Cliente.objects.exclude(nif__startswith="74")


# UD3.6e - Operación 5: el DNI del cliente se almacena en nif.
def get_cliente_dni_apellido():
    return Cliente.objects.filter(nif="92436593F", apellidos__contains="Pérez")


# UD3.6f - Operación 6: la descripción se refiere al id de Factura.
def get_cli_id_lt_2_num_fact_des():
    return Factura.objects.filter(id__lt=2).order_by("-numero")


# UD3.6g - Operación 7
def get_cli_id_gt_2():
    return Cliente.objects.filter(id__gt=2)


# UD3.6h - Operación 8: la descripción pide número ascendente.
def get_fact_des_nom_des():
    return Factura.objects.filter(concepto__contains="PHP").order_by("numero")


# UD3.6i - Operación 9
def get_fact_not_1():
    return Factura.objects.exclude(numero__endswith="1")


# UD3.6j - Operación 10: interpretamos "contenga python" como el concepto.
def get_cobro_python_id2():
    return Cobro.objects.filter(factura__concepto__contains="python", id__endswith="2").first()


# UD3.6k - Operación 11
def get_cobro_fact6_not_manu():
    return Cobro.objects.filter(factura__numero__contains="06").exclude(
        factura__cliente__nombre__contains="Manu"
    )


# UD3.6l - Operación 12: mayor o igual, según la descripción.
def get_fact_gt_5():
    return Factura.objects.filter(total__gte=5)


# UD3.6m - Operación 13: ambos extremos incluidos.
def get_cobro_5_10():
    return Cobro.objects.filter(importe__range=(5, 10))


# UD3.6n - Operación 14: DNI con letra válida y correo de ejemplo único.
def create_cliente():
    return Cliente.objects.create(
        nombre="Nuevo", apellidos="apellido1 apellido2",
        nif="12345678Z", email="nuevo@example.com"
    )


# UD3.6o - Operación 15: ejecutar después de create_cliente.
def create_factura():
    cliente = Cliente.objects.get(nif="12345678Z")
    return Factura.objects.create(
        cliente=cliente, numero="ORM-" + uuid4().hex[:16],
        concepto="Factura de práctica ORM",
        fecha=timezone.localdate() - timedelta(days=1), total=Decimal("100.00")
    )


# UD3.6p - Operación 16: última creada, determinada por la clave primaria.
def update_last_factura():
    factura = Factura.objects.order_by("pk").last()
    if factura is not None:
        factura.concepto += "(última)"
        factura.save(update_fields=["concepto"])
    return factura


# UD3.6q - Operación 17: F actualiza el importe directamente en la BD.
def update_cobro_fact2_x2():
    return Cobro.objects.filter(factura__numero__endswith="2").update(importe=F("importe") * 2)


# UD3.6r - Operación 18: divisor decimal para evitar división entera en SQLite.
def update_cobro_fact1_cligonz_div2():
    return Cobro.objects.filter(
        factura__numero__endswith="1", factura__cliente__apellidos__contains="González"
    ).update(importe=F("importe") / 2.0)


# UD3.6s - Operación 19
def delete_cobro_fact_lt_1():
    return Cobro.objects.filter(factura__total__lt=1).delete()


# UD3.6t - Operación 20
def delete_cobro_cli_pablo():
    return Cobro.objects.filter(factura__cliente__nombre__contains="Pablo").delete()
