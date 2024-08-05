#!/bin/sh

# Ejecutar collectstatic para recopilar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar Gunicorn
gunicorn core.wsgi
