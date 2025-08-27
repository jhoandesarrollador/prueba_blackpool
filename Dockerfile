# Usar una imagen base de Python delgada
FROM python:3.11-slim

# Actualizar los paquetes del sistema operativo para mitigar vulnerabilidades
# Se limpian los archivos de apt para mantener la imagen pequeña
RUN apt-get update && apt-get upgrade -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Establecer variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer el directorio de trabajo
WORKDIR /app

# Crear un grupo y usuario no root para ejecutar la aplicación
# La sintaxis es para Debian/Ubuntu, la base de python:3.11-slim
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./app /app/app

# Cambiar el propietario del directorio de la aplicación al usuario no root
RUN chown -R appuser:appgroup /app

# Cambiar al usuario no root
USER appuser

# Exponer el puerto en el que se ejecuta la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
