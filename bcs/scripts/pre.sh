#!/bin/bash
# Format staged files safely

# JS/CSS
git diff --name-only --cached -z | grep -zE '\.(js|css)$' | xargs -0 prettier --write --list-different

# HTML (Jinja/Django templates)
git diff --name-only --cached -z | grep -zE '\.html$' | xargs -0 djlint --reformat

# Python
git diff --name-only --cached -z | grep -zE '\.py$' | xargs -0 black -l 79
