#!/bin/bash
# Script to run/stop SCSS watchers for a given app

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/bcs" || exit 1

if [[ -n $1 ]]; then
  # Start watcher for provided app
  app="$1"
  echo "Starting SCSS watcher for $app..."
  nohup sass --watch "$app/static/$app/scss:$app/static/$app/css" >/dev/null 2>&1 &
  echo "Watcher started in background."
else
  # Stop all running Sass watchers
  echo "Stopping all SCSS watchers..."
  # Use pkill to kill sass processes with --watch argument
  pkill -f "sass --watch"
  echo "All watchers stopped."
fi
