#!/bin/bash
# Script to automate backup, migrations and running the server - "quick run"
set -euo pipefail
# -e: exit immediately on error
# -u: treat unset variables as errors
# -o pipefail: catch errors in piped commands

# Get optional label argument
label=${1:-}

# Step 1: Backup the database state before migrations
backup "$label"

# Step 2: Create migrations
python manage.py makemigrations

# Step 3: Apply migrations
python manage.py migrate

# Step 4: Run the Django development server
python manage.py runserver
