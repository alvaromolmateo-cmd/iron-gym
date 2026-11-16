from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect


# UD4.2i - Ordenación opcional por id, compartida por los listados.
class OrdenacionMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.GET.get('ordering')
        if ordering == 'asc':
            return queryset.order_by('id')
        if ordering == 'desc':
            return queryset.order_by('-id')
        return queryset


# UD4.2d - Contexto compartido por los formularios de creación y actualización.
class CrearActualizarMixin(SuccessMessageMixin):
    # UD4.4a - Mensaje común con la representación textual del objeto guardado.
    def get_success_message(self, cleaned_data):
        return self.success_message.format(self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_creacion'] = self.titulo_creacion
        context['titulo_actualizacion'] = self.titulo_actualizacion
        context['url_borrado'] = self.url_borrado
        return context


# UD4.2e - Contexto de la plantilla común de confirmación de borrado.
class ConfirmarBorradoMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        context['mensaje_confirmacion'] = self.mensaje_confirmacion
        return context


# UD4.2f - Informar de las relaciones PROTECT que impiden eliminar el objeto.
class BorradoProtegidoMixin:
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                'Existen dependencias para el objeto {}. Elimine antes dichas dependencias.'.format(self.object),
            )
            return HttpResponseRedirect(self.get_success_url())
