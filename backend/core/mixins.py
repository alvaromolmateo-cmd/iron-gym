from django.contrib import messages


# UD4.2h - Validar el horario tanto al crear como al actualizar.
class HorarioMixin:
    def form_valid(self, form):
        if form.instance.hora_cierre <= form.instance.hora_apertura:
            messages.error(self.request, 'La hora de cierre debe ser posterior a la hora de apertura.')
            return super().form_invalid(form)
        return super().form_valid(form)


# UD4.2h - Validar el intervalo del bloqueo en ambas vistas de edición.
class BloqueoMixin:
    def form_valid(self, form):
        if form.instance.fin <= form.instance.inicio:
            messages.error(self.request, 'El fin del bloqueo debe ser posterior al inicio.')
            return super().form_invalid(form)
        return super().form_valid(form)
