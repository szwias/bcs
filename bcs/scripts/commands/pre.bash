#!/bin/bash
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root" || exit 1

# JS/CSS/JSON
git diff --name-only -z |
  grep -zE '\.(js|css|scss|json)$' |
  xargs -0 --no-run-if-empty prettier --write --list-different

# HTML
git diff --name-only -z |
  grep -zE '\.html$' |
  xargs -0 --no-run-if-empty djlint --reformat

# Python
git diff --name-only -z |
  grep -zE '\.py$' |
  xargs -0 --no-run-if-empty black -l 79

# Bash
git diff --name-only -z |
  grep -zE '\.bash$' |
  xargs -0 --no-run-if-empty shfmt -w -i 2
