#!/bin/bash
# Script to automate backup, migrations and running the server - "quick run"

# Backup the database state before migrations
label=$1
backup "$label"

# Translate changes to migrations
python manage.py makemigrations

# Migrate changes to database
python manage.py migrate

# Run Django server
python manage.py runserver
