# UD5.3 - Aplicar login_required a dispatch para proteger las vistas de clase.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# UD4.2h - Validaciones propias reutilizadas en crear y actualizar.
from .mixins import HorarioMixin, BloqueoMixin
# UD4.3a - Formularios definidos en la app, siguiendo el apartado 4.1 del PDF.
from .forms import PerfilForm, InstalacionForm, HorarioForm, ReservaForm, BloqueoForm
# UD4.2i - Ordenacion opcional de los listados.
from common.mixins import OrdenacionMixin
# UD4.2d / UD4.2e / UD4.2f - Mixins compartidos por las vistas de mantenimiento.
from common.mixins import CrearActualizarMixin, ConfirmarBorradoMixin, BorradoProtegidoMixin
# UD3.7a - Vistas de consulta de core.
from django.views.generic import ListView, DetailView
# UD4.2a - Vistas de edicion genericas y redirecciones (PDF, apartados 3.1-3.4).
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo


# UD3.7a - Lista de Perfil.
@method_decorator(login_required, name="dispatch")
class PerfilListView(OrdenacionMixin, ListView):
    model = Perfil
    template_name = "core/perfil_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Perfil._meta.ordering, "pk"]


# UD3.7a - Detalle de Perfil.
@method_decorator(login_required, name="dispatch")
class PerfilDetailView(DetailView):
    model = Perfil
    template_name = "core/perfil_detail.html"


# UD3.7a - Lista de Instalacion.
@method_decorator(login_required, name="dispatch")
class InstalacionListView(OrdenacionMixin, ListView):
    model = Instalacion
    template_name = "core/instalacion_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Instalacion._meta.ordering, "pk"]


# UD3.7a - Detalle de Instalacion.
@method_decorator(login_required, name="dispatch")
class InstalacionDetailView(DetailView):
    model = Instalacion
    template_name = "core/instalacion_detail.html"


# UD3.7a - Lista de Horario.
@method_decorator(login_required, name="dispatch")
class HorarioListView(OrdenacionMixin, ListView):
    model = Horario
    template_name = "core/horario_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Horario._meta.ordering, "pk"]


# UD3.7a - Detalle de Horario.
@method_decorator(login_required, name="dispatch")
class HorarioDetailView(DetailView):
    model = Horario
    template_name = "core/horario_detail.html"


# UD3.7a - Lista de Reserva.
@method_decorator(login_required, name="dispatch")
class ReservaListView(OrdenacionMixin, ListView):
    model = Reserva
    template_name = "core/reserva_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Reserva._meta.ordering, "pk"]


# UD3.7a - Detalle de Reserva.
@method_decorator(login_required, name="dispatch")
class ReservaDetailView(DetailView):
    model = Reserva
    template_name = "core/reserva_detail.html"


# UD3.7a - Lista de Bloqueo.
@method_decorator(login_required, name="dispatch")
class BloqueoListView(OrdenacionMixin, ListView):
    model = Bloqueo
    template_name = "core/bloqueo_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Bloqueo._meta.ordering, "pk"]


# UD3.7a - Detalle de Bloqueo.
@method_decorator(login_required, name="dispatch")
class BloqueoDetailView(DetailView):
    model = Bloqueo
    template_name = "core/bloqueo_detail.html"


# UD4.2a - CreateView de Perfil, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class PerfilCreateView(CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear perfil"
    titulo_actualizacion = "Actualizar perfil"
    url_borrado = None
    model = Perfil
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = PerfilForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("perfil_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Perfil, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class PerfilUpdateView(CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear perfil"
    titulo_actualizacion = "Actualizar perfil"
    url_borrado = 'perfil_delete'
    model = Perfil
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = PerfilForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("perfil_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Perfil, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class PerfilDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar perfil"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Perfil
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("perfil_list")


# UD4.2a - CreateView de Instalacion, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class InstalacionCreateView(CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear instalacion"
    titulo_actualizacion = "Actualizar instalacion"
    url_borrado = None
    model = Instalacion
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = InstalacionForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("instalacion_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Instalacion, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class InstalacionUpdateView(CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear instalacion"
    titulo_actualizacion = "Actualizar instalacion"
    url_borrado = 'instalacion_delete'
    model = Instalacion
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = InstalacionForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("instalacion_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Instalacion, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class InstalacionDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar instalacion"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Instalacion
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("instalacion_list")


# UD4.2a - CreateView de Horario, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class HorarioCreateView(HorarioMixin, CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear horario"
    titulo_actualizacion = "Actualizar horario"
    url_borrado = None
    model = Horario
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = HorarioForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("horario_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Horario, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class HorarioUpdateView(HorarioMixin, CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear horario"
    titulo_actualizacion = "Actualizar horario"
    url_borrado = 'horario_delete'
    model = Horario
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = HorarioForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("horario_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Horario, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class HorarioDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar horario"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Horario
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("horario_list")


# UD4.2a - CreateView de Reserva, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class ReservaCreateView(CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear reserva"
    titulo_actualizacion = "Actualizar reserva"
    url_borrado = None
    model = Reserva
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = ReservaForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("reserva_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Reserva, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class ReservaUpdateView(CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear reserva"
    titulo_actualizacion = "Actualizar reserva"
    url_borrado = 'reserva_delete'
    model = Reserva
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = ReservaForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("reserva_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Reserva, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class ReservaDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar reserva"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Reserva
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("reserva_list")


# UD4.2a - CreateView de Bloqueo, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class BloqueoCreateView(BloqueoMixin, CrearActualizarMixin, CreateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} creado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear bloqueo"
    titulo_actualizacion = "Actualizar bloqueo"
    url_borrado = None
    model = Bloqueo
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = BloqueoForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("bloqueo_update", kwargs={"pk": self.object.pk})


# UD4.2a - UpdateView de Bloqueo, con formulario generado por Django.
@method_decorator(login_required, name="dispatch")
class BloqueoUpdateView(BloqueoMixin, CrearActualizarMixin, UpdateView):
    # UD4.4a - Mensaje tras guardar correctamente.
    success_message = "{} actualizado correctamente."
    # UD4.2c - Variables de la plantilla, enviadas por el mixin de UD4.2d.
    titulo_creacion = "Crear bloqueo"
    titulo_actualizacion = "Actualizar bloqueo"
    url_borrado = 'bloqueo_delete'
    model = Bloqueo
    # UD4.3a - form_class sustituye a fields en ambas vistas.
    form_class = BloqueoForm
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("bloqueo_update", kwargs={"pk": self.object.pk})


# UD4.2a - DeleteView de Bloqueo, con regreso a su listado.
@method_decorator(login_required, name="dispatch")
class BloqueoDeleteView(BorradoProtegidoMixin, ConfirmarBorradoMixin, DeleteView):
    # UD4.2e - Textos propios para la plantilla compartida.
    titulo = "Eliminar bloqueo"
    mensaje_confirmacion = "Confirma que deseas eliminar este objeto:"
    model = Bloqueo
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("bloqueo_list")
