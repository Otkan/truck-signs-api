#!/usr/bin/env bash
set -e

echo "Waiting for postgres to connect ..."

# Wait for the database to be up and ready, if not ready, then sleep for 5 seconds
while ! nc -z db 5432; do
  #TODO: Add missing implementation
done

echo "PostgreSQL is active"

python manage.py collectstatic --noinput

#TODO add migrations
echo "Postgresql migrations finished"

gunicorn tsa_app.wsgi:application --bind 0.0.0.0:8000
