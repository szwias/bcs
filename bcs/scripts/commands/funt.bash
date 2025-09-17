#!/bin/bash
# Script for formatting relevant yet untracked code
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/bcs/" || exit 1

prettier --write --list-different "**/media/**/*.json"
