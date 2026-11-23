from django.apps import AppConfig


# UD5.1 - App dedicada al modelo de usuario.
class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
