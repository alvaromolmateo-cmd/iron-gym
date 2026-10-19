from django.urls import re_path

from . import views

urlpatterns = [
    # Acepta /api/health y /api/health/
    re_path(r"^health/?$", views.health, name="health"),
]
