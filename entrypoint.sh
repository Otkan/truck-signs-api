#!/usr/bin/env bash
set -e

echo "Waiting for postgres to connect ..."

while ! nc -z "${DB_HOST}" "${DB_PORT}"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 5
done

echo "PostgreSQL is active"

cd /app/src

python manage.py migrate --noinput
echo "PostgreSQL migrations finished"

python manage.py collectstatic --noinput

python manage.py shell << EOF
from django.contrib.auth import get_user_model

User = get_user_model()

username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created")
    else:
        print("Superuser already exists - skipping")
else:
    print("Superuser env variables missing - skipping")
EOF

exec gunicorn tsa_app.wsgi:application --bind 0.0.0.0:8000