# UD5.3 - Aplicar login_required a dispatch para proteger las vistas de clase.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# UD4.3a - Formularios definidos en la app, siguiendo el apartado 4.1 del PDF.
from .forms import ClienteForm, FacturaForm, CobroForm
# UD4.2i - Ordenacion opcional de los listados.
from common.mixins import OrdenacionMixin
# UD4.2g - Validacion reutilizada en los cobros.
from .mixins import CobroMixin
# UD4.2d / UD4.2e / UD4.2f - Mixins compartidos por las vistas de mantenimiento.
from common.mixins import CrearActualizarMixin, ConfirmarBorradoMixin, BorradoProtegidoMixin
# UD3.7a - Vistas de consulta de billing.
from django.views.generic import ListView, DetailView
# UD4.2a - Vistas de edicion genericas y redirecciones (PDF, apartados 3.1-3.4).
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente, Factura, Cobro


# UD3.7a - Lista de Cliente.
@method_decorator(login_required, name="dispatch")
class ClienteListView(OrdenacionMixin, ListView):
    model = Cliente
    template_name = "billing/cliente_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Cliente._meta.ordering, "pk"]


# UD3.7a - Detalle de Cliente.
@method_decorator(login_required, name="dispatch")
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "billing/cliente_detail.html"


# UD3.7a - Lista de Factura.
@method_decorator(login_required, name="dispatch")
class FacturaListView(OrdenacionMixin, ListView):
    model = Factura
    template_name = "billing/factura_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Factura._meta.ordering, "pk"]


# UD3.7a - Detalle de Factura.
@method_decorator(login_required, name="dispatch")
class FacturaDetailView(DetailView):
    model = Factura
    template_name = "billing/factura_detail.html"


# UD3.7a - Lista de Cobro.
@method_decorator(login_required, name="dispatch")
class CobroListView(OrdenacionMixin, ListView):
    model = Cobro
    template_name = "billing/cobro_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Cobro._meta.ordering, "pk"]


# UD3.7a - Detalle de Cobro.
@method_decorator(login_required, name="dispatch")
class CobroDetailView(DetailView):
    model = Cobro
    template_name = "billing/cobro_detail.html"


# UD4.2a - CreateView de Cliente, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class ClienteCreateView(CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear cliente"
    titulo_actualizacion = "Actualizar cliente"
    url_borrado = None
    model = Cliente
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = ClienteForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cliente_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Cliente, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class ClienteUpdateView(CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear cliente"
    titulo_actualizacion = "Actualizar cliente"
    url_borrado = 'cliente_delete'
    model = Cliente
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = ClienteForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cliente_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Cliente, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class ClienteDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar cliente"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Cliente
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("cliente_list")


# UD4.2a - CreateView de Factura, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class FacturaCreateView(CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear factura"
    titulo_actualizacion = "Actualizar factura"
    url_borrado = None
    model = Factura
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = FacturaForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("factura_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Factura, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class FacturaUpdateView(CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear factura"
    titulo_actualizacion = "Actualizar factura"
    url_borrado = 'factura_delete'
    model = Factura
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = FacturaForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("factura_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Factura, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class FacturaDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar factura"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Factura
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("factura_list")


# UD4.2a - CreateView de Cobro, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class CobroCreateView(CobroMixin, CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear cobro"
    titulo_actualizacion = "Actualizar cobro"
    url_borrado = None
    model = Cobro
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = CobroForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cobro_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Cobro, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class CobroUpdateView(CobroMixin, CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear cobro"
    titulo_actualizacion = "Actualizar cobro"
    url_borrado = 'cobro_delete'
    model = Cobro
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = CobroForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("cobro_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Cobro, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class CobroDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar cobro"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Cobro
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("cobro_list")
