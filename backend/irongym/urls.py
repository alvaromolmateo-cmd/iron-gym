from django.contrib import admin
from django.urls import path
# UD3.2e - Ficheros multimedia en desarrollo.
from django.conf import settings
from django.conf.urls.static import static
# UD3.7b - Vistas comunes, de facturación y de Iron Gym.
from common import views as common_views
from billing import views as billing_views
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
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
]

# UD3.2e - Servir media solo en desarrollo.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
