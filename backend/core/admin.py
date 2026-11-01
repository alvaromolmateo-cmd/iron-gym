from django.contrib import admin

from .models import Perfil, Instalacion, Horario, Reserva, Bloqueo


# UD3.4c - Administrador del modelo Perfil
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'dni', 'telefono', 'fecha_alta', 'fecha_caducidad')
    list_display_links = ('usuario', 'dni')
    list_filter = ('tipo',)
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'dni')
    preserve_filters = True


# UD3.4c - Administrador del modelo Instalacion
@admin.register(Instalacion)
class InstalacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'capacidad', 'activa')
    list_display_links = ('nombre',)
    list_editable = ('activa',)  # UD3.4a - Columnas editables directamente desde la lista
    list_filter = ('tipo', 'activa')
    search_fields = ('nombre', 'descripcion')
    preserve_filters = True


# UD3.4c - Administrador del modelo Horario
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('instalacion', 'dia_semana', 'hora_apertura', 'hora_cierre', 'duracion_franja')
    list_display_links = ('instalacion', 'dia_semana')
    list_filter = ('instalacion', 'dia_semana')
    search_fields = ('instalacion__nombre',)
    preserve_filters = True


# UD3.4c - Administrador del modelo Reserva
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('instalacion', 'fecha', 'hora_inicio', 'hora_fin', 'usuario', 'estado')
    list_display_links = ('instalacion', 'fecha')
    list_filter = ('estado', 'instalacion', 'fecha')
    search_fields = ('instalacion__nombre', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    date_hierarchy = 'fecha'  # UD3.4a - Navegación por años, meses y días sobre un campo de fecha
    preserve_filters = True


# UD3.4c - Administrador del modelo Bloqueo
@admin.register(Bloqueo)
class BloqueoAdmin(admin.ModelAdmin):
    list_display = ('instalacion', 'inicio', 'fin', 'motivo', 'creado_por')
    list_display_links = ('instalacion', 'inicio')
    list_filter = ('instalacion',)
    search_fields = ('instalacion__nombre', 'motivo')
    date_hierarchy = 'inicio'
    preserve_filters = True
