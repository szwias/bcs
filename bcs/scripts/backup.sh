#!/bin/bash
# Script to backup current database

# Navigate to the 'baza' directory
cd baza || { echo "Directory 'baza' not found"; exit 1; }

# Move existing backup to the backups folder
mv baza.sql ./backups/baza.sql 2>/dev/null || echo "No existing baza.sql to move"

# Dump the PostgreSQL database
pg_dump -b -U postgres -f baza.sql bcs_db

# Return to the original directory
cd ..
