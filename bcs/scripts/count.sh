#!/bin/bash
# Script to count lines in different file types excluding certain directories

# Count lines in Python files excluding migrations
python_lines=$(find . -name '*.py' ! -path '*/migrations/*' -exec cat {} + | wc -l)
echo "Python lines: $python_lines"

# Count lines in SQL files excluding backups
sql_lines=$(find . -name '*.sql' ! -path '*/backups/*' -exec cat {} + | wc -l)
echo "SQL lines: $sql_lines"

# Count lines in HTML files
html_lines=$(find . -name '*.html' -exec cat {} + | wc -l)
echo "HTML lines: $html_lines"

# Count lines in shell files
bash_lines=$(find . -name '*.sh' -exec cat {} + | wc -l)
echo "Bash lines: $bash_lines"
