from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect

# UD4.2d - Mixin compartido.
class CrearActualizarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_creacion'] = self.titulo_creacion
        context['titulo_actualizacion'] = self.titulo_actualizacion
        context['url_borrado'] = self.url_borrado
        return context
