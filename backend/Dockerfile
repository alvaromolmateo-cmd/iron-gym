# UD3.2h Imagen base con la misma versión de Python que piapp-env
FROM python:3.13-slim

# UD3.2h Sin ficheros .pyc y con la salida de logs inmediata
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# UD3.2h Primero las dependencias, para aprovechar la caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# UD3.2h Después el código del proyecto
COPY . .

EXPOSE 8000

# UD3.2h Aplica migraciones, recoge estáticos y arranca el servidor accesible desde fuera del contenedor
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
