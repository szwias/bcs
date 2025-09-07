#!/bin/bash
# -----------------------------------------------------------------------------
# Script: create_cli_command.sh
# Description:
#   Converts a specified file into a CLI command:
#     - strips the last 3 characters from its name
#     - copies it to the virtualenv bin directory
#     - makes it executable
#     - optionally creates a symlink in scripts/command_links
# -----------------------------------------------------------------------------

set -euo pipefail

file="$1"
filename=$(basename "$file")
new_name="${filename:0:-3}"       # Remove last 3 chars
venv_bin="../.venv/bin"
symlink_dir="scripts/command_links"

# Copy file to venv bin
cp "$file" "$venv_bin/$new_name"

# Make executable
chmod +x "$venv_bin/$new_name"
echo "Created CLI command: $new_name"

# Create symlink if directory exists
mkdir -p "$symlink_dir"
ln -sf "$(realpath "$venv_bin/$new_name")" "$symlink_dir/$new_name"
echo "Created symlink to new command"
