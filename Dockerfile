FROM python:3.8-slim

# Instala las herramientas de desarrollo y dependencias necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    libpango1.0-0 \
    libgirepository1.0-dev \
    gobject-introspection \
    libxml2 \
    libxslt1.1 \
    libjpeg62-turbo \
    libgdk-pixbuf2.0-dev \
    libpangocairo-1.0-0

# Crea y activa un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia los archivos de la aplicación
COPY . /app
WORKDIR /app

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expon el puerto y corre la aplicación
EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
