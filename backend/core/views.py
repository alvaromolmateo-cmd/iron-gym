from django.db import connection
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    """Endpoint de prueba: confirma que la API responde y que hay conexión con la base de datos."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return Response({
        "status": "ok",
        "servicio": "Iron Gym API",
        "base_de_datos": connection.vendor,
        "hora": timezone.localtime().isoformat(),
    })
