# Usa una imagen de Python ligera pero estable
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias para Matplotlib y SQLite
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia primero los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto
COPY . .

# Crea la carpeta de datos por si no existe
RUN mkdir -p data

# Comando para ejecutar tu aplicación
CMD ["python", "main.py"]