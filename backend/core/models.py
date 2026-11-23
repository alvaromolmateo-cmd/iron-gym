# UD5.1 - Las relaciones usan el modelo de usuario configurado.
from django.conf import settings
from django.db import models
from django.utils import timezone

# UD3.3a - Tabla maestra ampliable desde el administrador, sin choices.
class TipoPerfil(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        # UD3.4e / UD3.4f - Nombres y orden del catálogo.
        verbose_name = 'tipo de perfil'
        verbose_name_plural = 'tipos de perfil'
        ordering = ['nombre']

    # UD3.3b - Etiqueta legible de la relación.
    def __str__(self):
        return self.nombre

# UD3.3a Modelo Perfil - Amplía el User de Django con el tipo de usuario
class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.ForeignKey('TipoPerfil', on_delete=models.PROTECT, default='socio')
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_caducidad = models.DateField(null=True, blank=True)

    class Meta:
        # UD3.4e - Nombre del modelo en el administrador
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        # UD3.4f - Ordenación por defecto: nombre de usuario
        ordering = ['usuario__username']

    # UD3.3b - Representación textual del perfil (Perfil)
    def __str__(self):
        return str(self.usuario) + ' (' + str(self.tipo) + ')'


# UD3.3a - Tabla maestra ampliable desde el administrador, sin choices.
class TipoInstalacion(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        # UD3.4e / UD3.4f - Nombres y orden del catálogo.
        verbose_name = 'tipo de instalación'
        verbose_name_plural = 'tipos de instalación'
        ordering = ['nombre']

    # UD3.3b - Etiqueta legible de la relación.
    def __str__(self):
        return self.nombre

# UD3.3a Modelo Instalacion - Pistas y salas reservables
class Instalacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.ForeignKey('TipoInstalacion', on_delete=models.PROTECT, default='pista')
    descripcion = models.TextField(blank=True)
    capacidad = models.PositiveIntegerField(default=1)
    activa = models.BooleanField(default=True)

    class Meta:
        # UD3.4e - Nombre del modelo en el administrador
        verbose_name = 'instalación'
        verbose_name_plural = 'instalaciones'
        # UD3.4f - Ordenación por defecto: nombre
        ordering = ['nombre']

    # UD3.3b - Representación textual de la instalación (Instalacion)
    def __str__(self):
        return self.nombre

# UD3.3a - Tabla maestra ampliable desde el administrador, sin choices.
class DiaSemana(models.Model):
    numero = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        # UD3.4e / UD3.4f - Nombres y orden del catálogo.
        verbose_name = 'día de la semana'
        verbose_name_plural = 'días de la semana'
        ordering = ['numero']

    # UD3.3b - Etiqueta legible de la relación.
    def __str__(self):
        return self.nombre

# UD3.3a Modelo Horario - Apertura semanal de cada instalación
class Horario(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    dia_semana = models.ForeignKey('DiaSemana', on_delete=models.PROTECT)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    duracion_franja = models.PositiveIntegerField(default=60)  # en minutos

    # UD3.3c - Una instalación solo tiene un horario por día de la semana
    class Meta:
        unique_together = [['instalacion', 'dia_semana']]
        # UD3.4e - Nombre del modelo en el administrador
        verbose_name = 'horario'
        verbose_name_plural = 'horarios'
        # UD3.4f - Ordenación por defecto: instalación y día de la semana
        ordering = ['instalacion__nombre', 'dia_semana']

    # UD3.3b - Representación textual del horario (Horario)
    def __str__(self):
        return (str(self.instalacion) + ' - ' + str(self.dia_semana) + ' '
                + self.hora_apertura.strftime('%H:%M') + '-' + self.hora_cierre.strftime('%H:%M'))

# UD3.3a - Tabla maestra ampliable desde el administrador, sin choices.
class EstadoReserva(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        # UD3.4e / UD3.4f - Nombres y orden del catálogo.
        verbose_name = 'estado de reserva'
        verbose_name_plural = 'estados de reserva'
        ordering = ['nombre']

    # UD3.3b - Etiqueta legible de la relación.
    def __str__(self):
        return self.nombre

# UD3.3a Modelo Reserva - Un usuario ocupa una instalación en una franja
class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instalacion = models.ForeignKey(Instalacion, on_delete=models.PROTECT)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.ForeignKey('EstadoReserva', on_delete=models.PROTECT, default='confirmada')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # UD3.3c - Una instalación no puede reservarse dos veces el mismo día a la misma hora
    class Meta:
        unique_together = [['instalacion', 'fecha', 'hora_inicio']]
        # UD3.4e - Nombre del modelo en el administrador
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        # UD3.4f - Ordenación por defecto: fecha descendente y hora de inicio
        ordering = ['-fecha', 'hora_inicio']

    # UD3.3b - Representación textual de la reserva (Reserva)
    def __str__(self):
        return (str(self.instalacion) + ' - ' + str(self.fecha) + ' '
                + self.hora_inicio.strftime('%H:%M') + ' (' + str(self.usuario) + ')')


# UD3.3a Modelo Bloqueo - Cierre temporal de una instalación
class Bloqueo(models.Model):
    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    # UD3.3c - No se puede registrar dos veces el mismo bloqueo de una instalación
    class Meta:
        unique_together = [['instalacion', 'inicio']]
        # UD3.4e - Nombre del modelo en el administrador
        verbose_name = 'bloqueo'
        verbose_name_plural = 'bloqueos'
        # UD3.4f - Ordenación por defecto: inicio descendente
        ordering = ['-inicio']

    # UD3.3b - Representación textual del bloqueo (Bloqueo)
    def __str__(self):
        return str(self.instalacion) + ' - ' + self.motivo
