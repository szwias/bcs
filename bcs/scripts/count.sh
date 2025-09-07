#!/bin/bash
# Script to count lines in different file types excluding certain directories

backup

sql_lines=$(find . -name '*.sql' \
    ! -path "*/scripts/other_locations*" \
    ! -path '*/backups/*' \
    -exec cat {} + | wc -l)

python_lines=$(find . -name '*.py' \
    ! -path "*/scripts/other_locations*" \
    ! -path '*/migrations/*' \
    -exec cat {} + | wc -l)

bash_lines=$(find . -name '*.sh' \
    ! -path "*/scripts/other_locations*" \
    -exec cat {} + | wc -l)

html_lines=$(find . -name '*.html' -exec cat {} + | wc -l)

css_lines=$(find . -name '*.css' \
   ! -path "*/staticfiles/*" \
   -exec cat {} + | wc -l)

js_lines=$(find . -name '*.js' \
   ! -path "*/staticfiles/*" \
   -exec cat {} + | wc -l)

json_lines=$(find . -name '*.json' -exec cat {} + | wc -l)

# Calculate totals
backend_lines=$((python_lines + bash_lines))
database_lines=$((sql_lines))
frontend_lines=$((html_lines + css_lines + js_lines))
media_lines=$((json_lines))
total_lines=$((backend_lines + database_lines + frontend_lines + media_lines))

WHITE="\033[0;97m"
START="\033[38;5;"
RESET="\033[0m"

# Map GitHub Linguist hex colors to closest 256-color codes
declare -A lang_colors=(
    ["SQL"]=172
    ["Python"]=25
    ["Bash"]=113
    ["HTML"]=166
    ["CSS"]=54
    ["JavaScript"]=221
    ["JSON"]=102
    ["Database"]=172
    ["Backend"]=25
    ["Frontend"]=166
    ["Media"]=102
)

# Function to calculate percentage
percentage() {
    awk "BEGIN { printf \"%.2f\", ($1/$total_lines)*100 }"
}

# Function to print aligned and colored output
print_colored() {
    local lang=$1
    local lines=$2
    local percent=$(percentage $lines)
    local color="${START}${lang_colors[$lang]}m"
    printf "$color%-10s | %7d | %6s%%${RESET}\n" "$lang" "$lines" "$percent"
}

print_group() {
    local group=$1
    local lines=$2
    local percent=$(percentage $lines)
    printf "%-10s | %7d | %6s%%\n" "$group" "$lines" "$percent"
}

# Print all lines
echo
print_colored "SQL" "$sql_lines"
print_colored "Python" "$python_lines"
print_colored "Bash" "$bash_lines"
print_colored "HTML" "$html_lines"
print_colored "CSS" "$css_lines"
print_colored "JavaScript" "$js_lines"
print_colored "JSON" "$json_lines"
echo
# Print grouped categories
print_group "Database" "$database_lines"
print_group "Backend" "$backend_lines"
print_group "Frontend" "$frontend_lines"
print_group "Media" "$media_lines"
