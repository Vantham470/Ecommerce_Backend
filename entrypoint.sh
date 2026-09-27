#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn Ecommerce_Backend.wsgi:application --bind 0.0.0.0:8000