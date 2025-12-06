#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
mkdir -p /app/staticfiles
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn bcs.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
