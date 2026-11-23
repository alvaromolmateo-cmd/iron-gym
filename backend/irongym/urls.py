from django.contrib import admin
from django.urls import path
# UD3.2e - Ficheros multimedia en desarrollo.
from django.conf import settings
from django.conf.urls.static import static
# UD3.7b - Vistas comunes, de facturación y de Iron Gym.
from common import views as common_views
from billing import views as billing_views
from core import views as core_views
# UD5.2b-c - Autenticación propia, anterior a la integración de Allauth.
from usuarios import views as usuarios_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", usuarios_views.UsuarioLoginView.as_view(), name="login"),
    path("logout/", usuarios_views.UsuarioLogoutView.as_view(), name="logout"),
    # UD3.7b - Inicio y panel.
    path("", common_views.HomeView.as_view(), name="home"),
    path("panel/", common_views.PanelView.as_view(), name="panel"),
    # UD3.7b - Rutas de Cliente.
    path("cliente_list/", billing_views.ClienteListView.as_view(), name="cliente_list"),
    path("cliente_detail/<int:pk>/", billing_views.ClienteDetailView.as_view(), name="cliente_detail"),
    # UD3.7b - Rutas de Factura.
    path("factura_list/", billing_views.FacturaListView.as_view(), name="factura_list"),
    path("factura_detail/<int:pk>/", billing_views.FacturaDetailView.as_view(), name="factura_detail"),
    # UD3.7b - Rutas de Cobro.
    path("cobro_list/", billing_views.CobroListView.as_view(), name="cobro_list"),
    path("cobro_detail/<int:pk>/", billing_views.CobroDetailView.as_view(), name="cobro_detail"),
    # UD3.7b - Rutas de Perfil.
    path("perfil_list/", core_views.PerfilListView.as_view(), name="perfil_list"),
    path("perfil_detail/<int:pk>/", core_views.PerfilDetailView.as_view(), name="perfil_detail"),
    # UD3.7b - Rutas de Instalacion.
    path("instalacion_list/", core_views.InstalacionListView.as_view(), name="instalacion_list"),
    path("instalacion_detail/<int:pk>/", core_views.InstalacionDetailView.as_view(), name="instalacion_detail"),
    # UD3.7b - Rutas de Horario.
    path("horario_list/", core_views.HorarioListView.as_view(), name="horario_list"),
    path("horario_detail/<int:pk>/", core_views.HorarioDetailView.as_view(), name="horario_detail"),
    # UD3.7b - Rutas de Reserva.
    path("reserva_list/", core_views.ReservaListView.as_view(), name="reserva_list"),
    path("reserva_detail/<int:pk>/", core_views.ReservaDetailView.as_view(), name="reserva_detail"),
    # UD3.7b - Rutas de Bloqueo.
    path("bloqueo_list/", core_views.BloqueoListView.as_view(), name="bloqueo_list"),
    path("bloqueo_detail/<int:pk>/", core_views.BloqueoDetailView.as_view(), name="bloqueo_detail"),
    # UD4.2b - Rutas de creacion, actualizacion y borrado.
    path("cliente_create/", billing_views.ClienteCreateView.as_view(), name="cliente_create"),
    path("cliente_update/<int:pk>/", billing_views.ClienteUpdateView.as_view(), name="cliente_update"),
    path("cliente_delete/<int:pk>/", billing_views.ClienteDeleteView.as_view(), name="cliente_delete"),
    path("factura_create/", billing_views.FacturaCreateView.as_view(), name="factura_create"),
    path("factura_update/<int:pk>/", billing_views.FacturaUpdateView.as_view(), name="factura_update"),
    path("factura_delete/<int:pk>/", billing_views.FacturaDeleteView.as_view(), name="factura_delete"),
    path("cobro_create/", billing_views.CobroCreateView.as_view(), name="cobro_create"),
    path("cobro_update/<int:pk>/", billing_views.CobroUpdateView.as_view(), name="cobro_update"),
    path("cobro_delete/<int:pk>/", billing_views.CobroDeleteView.as_view(), name="cobro_delete"),
    path("perfil_create/", core_views.PerfilCreateView.as_view(), name="perfil_create"),
    path("perfil_update/<int:pk>/", core_views.PerfilUpdateView.as_view(), name="perfil_update"),
    path("perfil_delete/<int:pk>/", core_views.PerfilDeleteView.as_view(), name="perfil_delete"),
    path("instalacion_create/", core_views.InstalacionCreateView.as_view(), name="instalacion_create"),
    path("instalacion_update/<int:pk>/", core_views.InstalacionUpdateView.as_view(), name="instalacion_update"),
    path("instalacion_delete/<int:pk>/", core_views.InstalacionDeleteView.as_view(), name="instalacion_delete"),
    path("horario_create/", core_views.HorarioCreateView.as_view(), name="horario_create"),
    path("horario_update/<int:pk>/", core_views.HorarioUpdateView.as_view(), name="horario_update"),
    path("horario_delete/<int:pk>/", core_views.HorarioDeleteView.as_view(), name="horario_delete"),
    path("reserva_create/", core_views.ReservaCreateView.as_view(), name="reserva_create"),
    path("reserva_update/<int:pk>/", core_views.ReservaUpdateView.as_view(), name="reserva_update"),
    path("reserva_delete/<int:pk>/", core_views.ReservaDeleteView.as_view(), name="reserva_delete"),
    path("bloqueo_create/", core_views.BloqueoCreateView.as_view(), name="bloqueo_create"),
    path("bloqueo_update/<int:pk>/", core_views.BloqueoUpdateView.as_view(), name="bloqueo_update"),
    path("bloqueo_delete/<int:pk>/", core_views.BloqueoDeleteView.as_view(), name="bloqueo_delete"),
]

# UD3.2e - Servir media solo en desarrollo.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
