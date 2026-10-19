from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Bloqueo, Horario, Instalacion, Reserva, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "rol", "is_active")
    list_filter = ("rol", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Iron Gym", {"fields": ("rol", "telefono")}),)


@admin.register(Instalacion)
class InstalacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "capacidad", "activa")
    list_filter = ("tipo", "activa")
    search_fields = ("nombre",)


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("instalacion", "dia_semana", "hora_apertura", "hora_cierre", "duracion_franja")
    list_filter = ("instalacion", "dia_semana")


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("instalacion", "fecha", "hora_inicio", "hora_fin", "usuario", "estado")
    list_filter = ("estado", "instalacion", "fecha")
    search_fields = ("usuario__username", "instalacion__nombre")


@admin.register(Bloqueo)
class BloqueoAdmin(admin.ModelAdmin):
    list_display = ("instalacion", "inicio", "fin", "motivo", "creado_por")
    list_filter = ("instalacion",)
