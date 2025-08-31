#!/bin/bash
# Script to backup current database

# Navigate to the 'baza' directory
cd baza || { echo "Directory 'baza' not found"; exit 1; }

# Create timestamped filename
timestamp=$(date +"%Y%m%d_%H%M%S")
new_dump="baza_${timestamp}.sql"

# Move existing timestamped dump(s) to backups
for file in baza_*.sql; do
    if [[ -f "$file" ]]; then
        mv "$file" "./backups/$file"
    fi
done

# Dump the PostgreSQL database into new timestamped file
pg_dump -b -U postgres -f "$new_dump" bcs_db

# Return to the original directory
cd ..
