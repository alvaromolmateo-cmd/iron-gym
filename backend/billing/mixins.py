from django.contrib import messages
from .models import Cobro


# UD4.2g - Reutilizar la validación del importe en la creación y actualización.
class CobroMixin:
    def form_valid(self, form):
        factura = form.instance.factura
        cobros = Cobro.objects.filter(factura=factura)
        # Al editar, sustituimos el importe anterior; no lo sumamos dos veces.
        if form.instance.pk:
            cobros = cobros.exclude(pk=form.instance.pk)
        total_cobrado = form.instance.importe
        for cobro in cobros:
            total_cobrado += cobro.importe
        if total_cobrado > factura.total:
            messages.error(self.request, 'La suma de los cobros no puede superar el total de la factura.')
            return super().form_invalid(form)
        return super().form_valid(form)
