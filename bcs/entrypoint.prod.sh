#!/bin/sh
set -e

echo "Ensuring staticfiles directory exists..."
mkdir -p /app/staticfiles

echo "Applying database migrations..."
python manage.py migrate --noinput --fake

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn bcs.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info
