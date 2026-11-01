from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# UD3.3a Modelo Perfil - Amplía el User de Django con el tipo de usuario
class Perfil(models.Model):
    TIPOS = [
        ('admin', 'Administrador'),
        ('socio', 'Socio'),
        ('abono_dia', 'Abono de un día'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='socio')
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_caducidad = models.DateField(null=True, blank=True)


    # UD3.3b - Representación textual del perfil (Perfil)
    def __str__(self):
        return str(self.usuario) + ' (' + self.get_tipo_display() + ')'


# UD3.3a Modelo Instalacion - Pistas y salas reservables
class Instalacion(models.Model):
    TIPOS = [
        ('pista', 'Pista'),
        ('sala', 'Sala'),
        ('piscina', 'Piscina'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='pista')
    descripcion = models.TextField(blank=True)
    capacidad = models.PositiveIntegerField(default=1)
    activa = models.BooleanField(default=True)


    # UD3.3b - Representación textual de la instalación (Instalacion)
    def __str__(self):
        return self.nombre


# UD3.3a Modelo Horario - Apertura semanal de cada instalación
class Horario(models.Model):
    DIAS = [
        (0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'),
        (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo'),
    ]

    instalacion = models.ForeignKey(Instalacion, on_delete=models.CASCADE)
    dia_semana = models.PositiveSmallIntegerField(choices=DIAS)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    duracion_franja = models.PositiveIntegerField(default=60)  # en minutos


    # UD3.3b - Representación textual del horario (Horario)
    def __str__(self):
        return (str(self.instalacion) + ' - ' + self.get_dia_semana_display() + ' '
                + self.hora_apertura.strftime('%H:%M') + '-' + self.hora_cierre.strftime('%H:%M'))


# UD3.3a Modelo Reserva - Un usuario ocupa una instalación en una franja
class Reserva(models.Model):
    ESTADOS = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    instalacion = models.ForeignKey(Instalacion, on_delete=models.PROTECT)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='confirmada')
    fecha_creacion = models.DateTimeField(auto_now_add=True)


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
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    # UD3.3b - Representación textual del bloqueo (Bloqueo)
    def __str__(self):
        return str(self.instalacion) + ' - ' + self.motivo
