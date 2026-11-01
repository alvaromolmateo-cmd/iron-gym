# UD3.7a - Vistas de consulta de billing.
from django.views.generic import ListView, DetailView
from .models import Cliente, Factura, Cobro


# UD3.7a - Lista de Cliente.
class ClienteListView(ListView):
    model = Cliente
    template_name = "billing/cliente_list.html"


# UD3.7a - Detalle de Cliente.
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "billing/cliente_detail.html"


# UD3.7a - Lista de Factura.
class FacturaListView(ListView):
    model = Factura
    template_name = "billing/factura_list.html"


# UD3.7a - Detalle de Factura.
class FacturaDetailView(DetailView):
    model = Factura
    template_name = "billing/factura_detail.html"


# UD3.7a - Lista de Cobro.
class CobroListView(ListView):
    model = Cobro
    template_name = "billing/cobro_list.html"


# UD3.7a - Detalle de Cobro.
class CobroDetailView(DetailView):
    model = Cobro
    template_name = "billing/cobro_detail.html"
