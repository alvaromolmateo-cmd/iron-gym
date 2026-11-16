# UD4.2a - Vistas genericas de edicion y redirecciones.
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# UD3.7a - Vistas de consulta de core.
from django.views.generic import ListView, DetailView
from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo


# UD3.7a - Lista de Perfil.
class PerfilListView(ListView):
    model = Perfil
    template_name = "core/perfil_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Perfil._meta.ordering, "pk"]


# UD3.7a - Detalle de Perfil.
class PerfilDetailView(DetailView):
    model = Perfil
    template_name = "core/perfil_detail.html"


# UD3.7a - Lista de Instalacion.
class InstalacionListView(ListView):
    model = Instalacion
    template_name = "core/instalacion_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Instalacion._meta.ordering, "pk"]


# UD3.7a - Detalle de Instalacion.
class InstalacionDetailView(DetailView):
    model = Instalacion
    template_name = "core/instalacion_detail.html"


# UD3.7a - Lista de Horario.
class HorarioListView(ListView):
    model = Horario
    template_name = "core/horario_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Horario._meta.ordering, "pk"]


# UD3.7a - Detalle de Horario.
class HorarioDetailView(DetailView):
    model = Horario
    template_name = "core/horario_detail.html"


# UD3.7a - Lista de Reserva.
class ReservaListView(ListView):
    model = Reserva
    template_name = "core/reserva_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Reserva._meta.ordering, "pk"]


# UD3.7a - Detalle de Reserva.
class ReservaDetailView(DetailView):
    model = Reserva
    template_name = "core/reserva_detail.html"


# UD3.7a - Lista de Bloqueo.
class BloqueoListView(ListView):
    model = Bloqueo
    template_name = "core/bloqueo_list.html"
    # UD3.8b - Diez registros por página, con desempate por id.
    paginate_by = 10
    ordering = [*Bloqueo._meta.ordering, "pk"]


# UD3.7a - Detalle de Bloqueo.
class BloqueoDetailView(DetailView):
    model = Bloqueo
    template_name = "core/bloqueo_detail.html"


# UD4.2a - Vista de create de Perfil.
class PerfilCreateView(CreateView):
    model = Perfil
    fields = ['usuario', 'tipo', 'dni', 'telefono', 'fecha_alta', 'fecha_caducidad']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("perfil_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Perfil.
class PerfilUpdateView(UpdateView):
    model = Perfil
    fields = ['usuario', 'tipo', 'dni', 'telefono', 'fecha_alta', 'fecha_caducidad']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("perfil_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Perfil.
class PerfilDeleteView(DeleteView):
    model = Perfil
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("perfil_list")


# UD4.2a - Vista de create de Instalacion.
class InstalacionCreateView(CreateView):
    model = Instalacion
    fields = ['nombre', 'tipo', 'descripcion', 'capacidad', 'activa']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("instalacion_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Instalacion.
class InstalacionUpdateView(UpdateView):
    model = Instalacion
    fields = ['nombre', 'tipo', 'descripcion', 'capacidad', 'activa']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("instalacion_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Instalacion.
class InstalacionDeleteView(DeleteView):
    model = Instalacion
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("instalacion_list")


# UD4.2a - Vista de create de Horario.
class HorarioCreateView(CreateView):
    model = Horario
    fields = ['instalacion', 'dia_semana', 'hora_apertura', 'hora_cierre', 'duracion_franja']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("horario_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Horario.
class HorarioUpdateView(UpdateView):
    model = Horario
    fields = ['instalacion', 'dia_semana', 'hora_apertura', 'hora_cierre', 'duracion_franja']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("horario_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Horario.
class HorarioDeleteView(DeleteView):
    model = Horario
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("horario_list")


# UD4.2a - Vista de create de Reserva.
class ReservaCreateView(CreateView):
    model = Reserva
    fields = ['usuario', 'instalacion', 'fecha', 'hora_inicio', 'hora_fin', 'estado']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("reserva_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Reserva.
class ReservaUpdateView(UpdateView):
    model = Reserva
    fields = ['usuario', 'instalacion', 'fecha', 'hora_inicio', 'hora_fin', 'estado']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("reserva_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Reserva.
class ReservaDeleteView(DeleteView):
    model = Reserva
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("reserva_list")


# UD4.2a - Vista de create de Bloqueo.
class BloqueoCreateView(CreateView):
    model = Bloqueo
    fields = ['instalacion', 'inicio', 'fin', 'motivo', 'creado_por']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("bloqueo_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de update de Bloqueo.
class BloqueoUpdateView(UpdateView):
    model = Bloqueo
    fields = ['instalacion', 'inicio', 'fin', 'motivo', 'creado_por']
    template_name = "base_create_update.html"

    # UD4.2a - Tras guardar, volver a la edicion del objeto.
    def get_success_url(self):
        return reverse_lazy("bloqueo_update", kwargs={"pk": self.object.pk})


# UD4.2a - Vista de delete de Bloqueo.
class BloqueoDeleteView(DeleteView):
    model = Bloqueo
    template_name = "base_confirm_delete.html"
    success_url = reverse_lazy("bloqueo_list")
