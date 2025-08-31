#!/bin/bash
# Script to backup current database with per-day directories

# Navigate to the 'baza' directory
cd baza || { echo "Directory 'baza' not found"; exit 1; }

# Create today's date and timestamp
day=$(date +"%Y-%m-%d")
timestamp=$(date +"%Y%m%d_%H%M%S")
new_dump="baza_${timestamp}.sql"

# Ensure today's backup directory exists
mkdir -p "./backups/$day"

# Move any existing timestamped dump(s) into their respective day's folder
for file in baza_*.sql; do
    if [[ -f "$file" ]]; then
        # Extract YYYYMMDD from filename
        yyyymmdd=$(echo "$file" | grep -oP '\d{8}' | head -1)
        if [[ -n "$yyyymmdd" ]]; then
            # Convert YYYYMMDD -> YYYY-MM-DD
            file_day="${yyyymmdd:0:4}-${yyyymmdd:4:2}-${yyyymmdd:6:2}"
            mkdir -p "./backups/$file_day"
            mv "$file" "./backups/$file_day/"
        fi
    fi
done

# Create a fresh dump in the main 'baza' folder
pg_dump -b -U postgres -f "$new_dump" bcs_db

# Return to the original directory
cd ..
