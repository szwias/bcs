#!/bin/bash
# -----------------------------------------------------------------------------
# Script: add
# Description:
#   If a CLI command with the same name already exists in the virtualenv bin,
#   back it up to scripts/code_repr/<name>.sh.
#   Otherwise, copy the new script to the virtualenv bin, make it executable,
#   and create a symlink in scripts/.
#
# Usage:
#   add command_name
# -----------------------------------------------------------------------------

new_name="$1"
file="code_repr/$1.sh"
venv_bin="../.venv/bin"
symlink_dir="scripts"
backup_dir="scripts/code_repr"

# Check if the command already exists
if [[ -f "$venv_bin/$new_name" ]]; then
    echo "Command '$new_name' already exists in $venv_bin"
    mkdir -p "$backup_dir"
    cp "$venv_bin/$new_name" "$backup_dir/$new_name.sh"
    echo "Backed up existing command to $backup_dir/$new_name.sh"
else
    # Copy file to venv bin
    cp "$file" "$venv_bin/$new_name"

    # Make executable
    chmod +x "$venv_bin/$new_name"
    echo "Created CLI command: $new_name"

    # Create symlink
    mkdir -p "$symlink_dir"
    ln -sf "$(realpath "$venv_bin/$new_name")" "$symlink_dir/$new_name"
    echo "Created symlink to new command"
fi
