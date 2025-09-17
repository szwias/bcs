#!/bin/bash
# Script to backup current database with per-day directories
# Usage: backup [label]

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/bcs/baza" || {
  echo "Directory 'baza' not found"
  exit 1
}

# Create date components
day=$(date +"%Y-%m-%d")
timestamp=$(date +"%Y%m%d_%H%M%S")

# Optional argument (label) for the dump name
label=$1
if [[ -n $label ]]; then
  new_dump="baza_${timestamp}_${label}.sql"
else
  new_dump="baza_${timestamp}.sql"
fi

# Ensure today's backup directory exists
mkdir -p "./backups/$day"

# Move any existing timestamped dump(s) to their day's folder
for file in baza_*.sql; do
  if [[ -f $file ]]; then
    yyyymmdd=$(echo "$file" | grep -oP '\d{8}' | head -1)
    if [[ -n $yyyymmdd ]]; then
      file_day="${yyyymmdd:0:4}-${yyyymmdd:4:2}-${yyyymmdd:6:2}"
      mkdir -p "./backups/$file_day"
      mv "$file" "./backups/$file_day/"
    fi
  fi
done

# Create a fresh dump
pg_dump -b -U postgres -f "$new_dump" bcs_db || {
  echo "❌ Backup failed"
  exit 1
}

echo "✅ Backup created: $new_dump"

cd ..
