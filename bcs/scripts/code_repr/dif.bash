#!/bin/bash
# Shortcut script
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/bcs/" || exit 1

git diff >diff.txt
