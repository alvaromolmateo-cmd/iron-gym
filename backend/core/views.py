# UD3.7a - Vistas de consulta de core.
from django.views.generic import ListView, DetailView
from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo


# UD3.7a - Lista de Perfil.
class PerfilListView(ListView):
    model = Perfil
    template_name = "core/perfil_list.html"


# UD3.7a - Detalle de Perfil.
class PerfilDetailView(DetailView):
    model = Perfil
    template_name = "core/perfil_detail.html"


# UD3.7a - Lista de Instalacion.
class InstalacionListView(ListView):
    model = Instalacion
    template_name = "core/instalacion_list.html"


# UD3.7a - Detalle de Instalacion.
class InstalacionDetailView(DetailView):
    model = Instalacion
    template_name = "core/instalacion_detail.html"


# UD3.7a - Lista de Horario.
class HorarioListView(ListView):
    model = Horario
    template_name = "core/horario_list.html"


# UD3.7a - Detalle de Horario.
class HorarioDetailView(DetailView):
    model = Horario
    template_name = "core/horario_detail.html"


# UD3.7a - Lista de Reserva.
class ReservaListView(ListView):
    model = Reserva
    template_name = "core/reserva_list.html"


# UD3.7a - Detalle de Reserva.
class ReservaDetailView(DetailView):
    model = Reserva
    template_name = "core/reserva_detail.html"


# UD3.7a - Lista de Bloqueo.
class BloqueoListView(ListView):
    model = Bloqueo
    template_name = "core/bloqueo_list.html"


# UD3.7a - Detalle de Bloqueo.
class BloqueoDetailView(DetailView):
    model = Bloqueo
    template_name = "core/bloqueo_detail.html"
