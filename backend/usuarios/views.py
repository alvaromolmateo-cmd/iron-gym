from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm


# UD5.2a-b - Django comprueba credenciales y guarda la autenticación en la sesión.
# Fuente: https://docs.djangoproject.com/en/5.2/topics/auth/default/#authentication-views
class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm


# UD5.2c - LogoutView cierra la sesión mediante POST con protección CSRF.
class UsuarioLogoutView(LogoutView):
    next_page = 'home'
