#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating/updating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
username = 'Admin'
password = 'Vthborn2006'
email = 'vanthamtyrano@gmail.com'
if username and password:
    user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_superuser': True, 'is_staff': True})
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print('Superuser ready:', username)
"

echo "Starting Gunicorn..."
exec gunicorn Ecommerce_Backend.wsgi:application --bind 0.0.0.0:8000