#!/bin/bash
# -----------------------------------------------------------------------------
# Script: add
# Description:
#   Converts a specified script into a CLI command by:
#     - Copying the script from scripts/ to the virtual environment's bin directory
#     - Removing the .sh extension for the command name
#     - Making the file executable
#     - Creating a symlink in scripts/command_links for easy access
#
# Usage:
#   ./add command_name
#
# Assumes:
#   - Virtual environment located at ../.venv/
#   - Script is run from bcs/bcs/
#   - Original script is located in bcs/bcs/scripts/ and ends with .sh
#   - Write permissions to venv bin directory
# -----------------------------------------------------------------------------

new_name="$1"
file="scripts/$1.sh"
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
