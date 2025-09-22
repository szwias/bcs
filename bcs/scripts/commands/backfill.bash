#!/bin/bash
# Shortcut script
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/bcs/" || exit 1

python manage.py backfill_searchable_models
