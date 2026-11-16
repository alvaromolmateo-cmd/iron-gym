# UD4.2a - Vistas genericas de edicion y redirecciones.
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# UD3.7a - Vistas de consulta de billing.
from django.views.generic import ListView, DetailView
from .models import Cliente, Factura, Cobro


# UD3.7a - Lista de Cliente.
class ClienteListView(ListView):
    model = Cliente
    template_name = "billing/cliente_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Cliente._meta.ordering, "pk"]


# UD3.7a - Detalle de Cliente.
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "billing/cliente_detail.html"


# UD3.7a - Lista de Factura.
class FacturaListView(ListView):
    model = Factura
    template_name = "billing/factura_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Factura._meta.ordering, "pk"]


# UD3.7a - Detalle de Factura.
class FacturaDetailView(DetailView):
    model = Factura
    template_name = "billing/factura_detail.html"


# UD3.7a - Lista de Cobro.
class CobroListView(ListView):
    model = Cobro
    template_name = "billing/cobro_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Cobro._meta.ordering, "pk"]


# UD3.7a - Detalle de Cobro.
class CobroDetailView(DetailView):
    model = Cobro
    template_name = "billing/cobro_detail.html"


# UD4.2a - Vista de create de Cliente.
class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nombre', 'apellidos', 'nif', 'email']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cliente_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Cliente.
class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = ['nombre', 'apellidos', 'nif', 'email']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cliente_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Cliente.
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("cliente_list")


# UD4.2a - Vista de create de Factura.
class FacturaCreateView(CreateView):
    model = Factura
    fields = ['cliente', 'numero', 'concepto', 'fecha', 'total']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("factura_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Factura.
class FacturaUpdateView(UpdateView):
    model = Factura
    fields = ['cliente', 'numero', 'concepto', 'fecha', 'total']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("factura_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Factura.
class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("factura_list")


# UD4.2a - Vista de create de Cobro.
class CobroCreateView(CreateView):
    model = Cobro
    fields = ['factura', 'fecha', 'importe']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cobro_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Cobro.
class CobroUpdateView(UpdateView):
    model = Cobro
    fields = ['factura', 'fecha', 'importe']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cobro_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Cobro.
class CobroDeleteView(DeleteView):
    model = Cobro
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("cobro_list")
