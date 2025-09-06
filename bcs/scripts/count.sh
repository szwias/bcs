#!/bin/bash
# Script to count lines in different file types excluding certain directories

backup

echo
echo "BACKEND:"

# Count lines in Python files excluding migrations
python_lines=$(find . -name '*.py' \
    ! -path "*/scripts/other_locations*" \
    ! -path '*/migrations/*' \
    -exec cat {} + | wc -l)
echo "Python lines: $python_lines"

# Count lines in SQL files excluding backups
sql_lines=$(find . -name '*.sql' \
    ! -path "*/scripts/other_locations*" \
    ! -path '*/backups/*' \
    -exec cat {} + | wc -l)
echo "SQL lines: $sql_lines"

# Count lines in Bash files
bash_lines=$(find . -name '*.sh' \
    ! -path "*/scripts/other_locations*" \
    -exec cat {} + | wc -l)
echo "Bash lines: $bash_lines"

echo
echo "FRONTEND:"

# Count lines in HTML files
html_lines=$(find . -name '*.html' -exec cat {} + | wc -l)
echo "HTML lines: $html_lines"

# Count lines in CSS files
css_lines=$(find . -name '*.css' \
   ! -path "*/staticfiles/*" \
   -exec cat {} + | wc -l)
echo "CSS lines: $css_lines"

# Count lines in JS files
js_lines=$(find . -name '*.js' \
   ! -path "*/staticfiles/*" \
   -exec cat {} + | wc -l)
echo "JS lines: $js_lines"

echo
echo "MEDIA:"

# Count lines in JSON files
json_lines=$(find . -name '*.json' \
    -exec cat {} + | wc -l)
echo "JSON lines: $json_lines"

echo
