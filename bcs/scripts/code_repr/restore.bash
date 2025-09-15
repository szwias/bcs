#!/bin/bash
set -e # Safe exit on fail

# Dropping the database
psql -U postgres -c "DROP DATABASE IF EXISTS bcs_db"

# Creating the database
psql -U postgres -c "CREATE DATABASE bcs_db"

# Restoring the database
psql -U postgres -d bcs_db -f baza/baza.sql >/dev/null 2>&1

echo "Database restored successfully"
