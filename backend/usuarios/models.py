from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# UD5.1 - Manager basado en el Anexo I: email y contraseña cifrada.
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Ha de proporcionar un e-mail válido')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('activo', True)
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name or '',
            last_name=last_name or '',
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # UD5.1 - createsuperuser solicita el email como identificador.
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        for field in ('is_staff', 'is_active', 'is_superuser'):
            if extra_fields[field] is not True:
                raise ValueError('Un superusuario debe tener {}=True.'.format(field))
        return self.create_user(email=email, password=password, **extra_fields)


# UD5.1 - AbstractBaseUser y permisos estándar necesarios para el administrador.
# Fuente del enunciado: https://docs.djangoproject.com/en/5.2/topics/auth/customizing/
class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    activo = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # UD5.1 - Campos utilizados por el manager del anexo y el proyecto existente.
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    # UD5.1 - Identificación legible en el administrador y relaciones de core.
    def __str__(self):
        return self.email
