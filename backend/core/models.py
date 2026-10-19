from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Usuario(AbstractUser):
    """Usuario de la aplicación. El rol decide los permisos (socio o administrador)."""

    class Rol(models.TextChoices):
        SOCIO = "socio", "Socio"
        ADMIN = "admin", "Administrador"

    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.SOCIO, verbose_name="Rol")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN or self.is_superuser

    def __str__(self):
        return self.get_full_name() or self.username


class Instalacion(models.Model):
    """Pista o espacio reservable del centro (pádel, tenis, sala, piscina...)."""

    class Tipo(models.TextChoices):
        PISTA = "pista", "Pista"
        SALA = "sala", "Sala"
        PISCINA = "piscina", "Piscina"
        CAMPO = "campo", "Campo"
        OTRO = "otro", "Otro"

    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    tipo = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.PISTA, verbose_name="Tipo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    capacidad = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name="Capacidad (personas)"
    )
    activa = models.BooleanField(default=True, verbose_name="Activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Instalación"
        verbose_name_plural = "Instalaciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    """Horario de apertura de una instalación para un día de la semana, dividido en franjas."""

    class DiaSemana(models.IntegerChoices):
        LUNES = 0, "Lunes"
        MARTES = 1, "Martes"
        MIERCOLES = 2, "Miércoles"
        JUEVES = 3, "Jueves"
        VIERNES = 4, "Viernes"
        SABADO = 5, "Sábado"
        DOMINGO = 6, "Domingo"

    instalacion = models.ForeignKey(
        Instalacion, on_delete=models.CASCADE, related_name="horarios", verbose_name="Instalación"
    )
    dia_semana = models.PositiveSmallIntegerField(choices=DiaSemana.choices, verbose_name="Día de la semana")
    hora_apertura = models.TimeField(verbose_name="Hora de apertura")
    hora_cierre = models.TimeField(verbose_name="Hora de cierre")
    duracion_franja = models.PositiveSmallIntegerField(
        default=60, validators=[MinValueValidator(15)], verbose_name="Duración de la franja (min)"
    )

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        ordering = ["instalacion", "dia_semana", "hora_apertura"]
        constraints = [
            models.UniqueConstraint(fields=["instalacion", "dia_semana"], name="horario_unico_por_dia"),
            models.CheckConstraint(condition=Q(hora_cierre__gt=models.F("hora_apertura")), name="horario_cierre_posterior"),
        ]

    def __str__(self):
        return f"{self.instalacion} · {self.get_dia_semana_display()} {self.hora_apertura:%H:%M}-{self.hora_cierre:%H:%M}"


class Reserva(models.Model):
    """Reserva de una franja de una instalación por parte de un usuario."""

    class Estado(models.TextChoices):
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservas", verbose_name="Usuario"
    )
    instalacion = models.ForeignKey(
        Instalacion, on_delete=models.PROTECT, related_name="reservas", verbose_name="Instalación"
    )
    fecha = models.DateField(verbose_name="Fecha")
    hora_inicio = models.TimeField(verbose_name="Hora de inicio")
    hora_fin = models.TimeField(verbose_name="Hora de fin")
    estado = models.CharField(
        max_length=10, choices=Estado.choices, default=Estado.CONFIRMADA, verbose_name="Estado"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["fecha", "hora_inicio"]
        constraints = [
            # Una misma instalación no puede tener dos reservas confirmadas que empiecen a la misma hora.
            models.UniqueConstraint(
                fields=["instalacion", "fecha", "hora_inicio"],
                condition=Q(estado="confirmada"),
                name="reserva_unica_por_franja",
            ),
            models.CheckConstraint(condition=Q(hora_fin__gt=models.F("hora_inicio")), name="reserva_fin_posterior"),
        ]

    def clean(self):
        if self.hora_inicio and self.hora_fin and self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la de inicio.")
        if not (self.instalacion_id and self.fecha and self.hora_inicio and self.hora_fin):
            return
        if self.estado != self.Estado.CONFIRMADA:
            return

        # Solapamiento con otras reservas confirmadas (cubre franjas que no empiezan a la misma hora).
        solapadas = Reserva.objects.filter(
            instalacion_id=self.instalacion_id,
            fecha=self.fecha,
            estado=self.Estado.CONFIRMADA,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio,
        ).exclude(pk=self.pk)
        if solapadas.exists():
            raise ValidationError("La instalación ya está reservada en esa franja horaria.")

        # Solapamiento con bloqueos por mantenimiento.
        inicio = datetime.combine(self.fecha, self.hora_inicio)
        fin = datetime.combine(self.fecha, self.hora_fin)
        if settings.USE_TZ:
            inicio, fin = timezone.make_aware(inicio), timezone.make_aware(fin)
        if Bloqueo.objects.filter(instalacion_id=self.instalacion_id, inicio__lt=fin, fin__gt=inicio).exists():
            raise ValidationError("La instalación está bloqueada por mantenimiento en esa franja.")

    def __str__(self):
        return f"{self.instalacion} · {self.fecha} {self.hora_inicio:%H:%M} · {self.usuario}"


class Bloqueo(models.Model):
    """Periodo en el que una instalación no se puede reservar (mantenimiento, eventos...)."""

    instalacion = models.ForeignKey(
        Instalacion, on_delete=models.CASCADE, related_name="bloqueos", verbose_name="Instalación"
    )
    inicio = models.DateTimeField(verbose_name="Inicio")
    fin = models.DateTimeField(verbose_name="Fin")
    motivo = models.CharField(max_length=200, verbose_name="Motivo")
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bloqueos_creados",
        verbose_name="Creado por",
    )

    class Meta:
        verbose_name = "Bloqueo"
        verbose_name_plural = "Bloqueos"
        ordering = ["-inicio"]
        constraints = [
            models.CheckConstraint(condition=Q(fin__gt=models.F("inicio")), name="bloqueo_fin_posterior"),
        ]

    def __str__(self):
        return f"{self.instalacion} bloqueada {self.inicio:%d/%m/%Y %H:%M} - {self.fin:%d/%m/%Y %H:%M}"
