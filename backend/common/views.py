# UD5.3 - Aplicar login_required a dispatch para proteger las vistas de clase.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# UD3.7a - Páginas comunes de la aplicación.
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "common/home.html"


@method_decorator(login_required, name="dispatch")
class PanelView(TemplateView):
    template_name = "common/panel.html"
