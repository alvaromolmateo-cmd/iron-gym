# UD3.7a - Páginas comunes de la aplicación.
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "common/home.html"


class PanelView(TemplateView):
    template_name = "common/panel.html"
