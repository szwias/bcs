#!/bin/bash
# -----------------------------------------------------------------------------
# Script: add
# Description:
#   Format all shell scripts from bcs/scripts/code_repr, copy them to .venv/bin/
#   and make executable; create symlinks to those executables in bcs/scripts/
#
# Usage: add
# -----------------------------------------------------------------------------

set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/" || exit 1

venv_bin=".venv/bin"
symlink_dir="bcs/scripts"
scripts_dir="bcs/scripts/code_repr"

mkdir -p "$venv_bin" "$symlink_dir"

shopt -s nullglob
for file in "$scripts_dir"/*; do
  [ -f "$file" ] || continue

  # Format file
  shfmt -w -i 2 -s "$file"

  # Extract its name
  basename="${file##*/}"
  name="${basename%%.*}"

  # Copy the file to venv bin
  cp "$file" "$venv_bin/$name"

  # Make it executable
  chmod +x "$venv_bin/$name"
  echo "✅ Created CLI command: $name"

  # Create symlink
  ln -sf "$(realpath "$venv_bin/$name")" "$symlink_dir/$name"
  echo "🔗 Created symlink: $symlink_dir/$name"
done
shopt -u nullglob
