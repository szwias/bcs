#!/bin/bash
# Script to count lines in different file types excluding certain directories

backup

# Count lines
sql_lines=$(find . -name '*.sql' \
    ! -path '*/backups/*' \
    -exec cat {} + | wc -l)

python_lines=$(find . -name '*.py' \
    ! -path '*/migrations/*' \
    -exec cat {} + | wc -l)

bash_lines=$(find . -name '*.sh' \
    -exec cat {} + | wc -l)

html_lines=$(find . -name '*.html' -exec cat {} + | wc -l)

css_lines=$(find . -name '*.css' \
   ! -path "*/staticfiles/*" \
   -exec cat {} + | wc -l)

js_lines=$(find . -name '*.js' \
   ! -path "*/staticfiles/*" \
   -exec cat {} + | wc -l)

json_lines=$(find . -name '*.json' -exec cat {} + | wc -l)

# Totals
backend_lines=$((python_lines + bash_lines))
database_lines=$((sql_lines))
frontend_lines=$((html_lines + css_lines + js_lines))
media_lines=$((json_lines))
total_lines=$((backend_lines + database_lines + frontend_lines + media_lines))

echo
echo "Total lines: $total_lines"

# Colors
START="\033[38;5;"
RESET="\033[0m"

declare -A lang_colors=(
    ["SQL"]=172
    ["Python"]=25
    ["Bash"]=113
    ["HTML"]=166
    ["CSS"]=54
    ["JS"]=221
    ["JSON"]=102
    ["Database"]=172
    ["Backend"]=25
    ["Frontend"]=166
    ["Media"]=102
)

# Percentage calculation (safe for zero values)
percentage() {
    local value="${1:-0}"
    awk -v val="$value" -v total="$total_lines" \
        'BEGIN { printf "%.2f", (total==0 ? 0 : (val/total)*100) }'
}

# Print colored line
print_colored() {
    local lang=$1
    local lines=$2
    local percent=$(percentage "$lines")
    local color="${START}${lang_colors[$lang]}m"
    printf "$color%-10s | %7d | %6s%%${RESET}\n" "$lang" "$lines" "$percent"
}

# Print uncolored group line
print_group() {
    local group=$1
    local lines=$2
    local percent=$(percentage "$lines")
    printf "%-10s | %7d | %6s%%\n" "$group" "$lines" "$percent"
}

# -----------------------------
# Sort and print languages
# -----------------------------
declare -a lang_list
for lang in SQL Python Bash HTML CSS JS JSON; do
    lines_var="${lang,,}_lines"
    lines="${!lines_var:-0}"
    percent=$(percentage "$lines")
    lang_list+=("$percent|$lang|$lines")
done

IFS=$'\n' sorted_langs=($(sort -t '|' -k1 -nr <<<"${lang_list[*]}"))
unset IFS

echo
for entry in "${sorted_langs[@]}"; do
    IFS='|' read -r percent lang lines <<< "$entry"
    print_colored "$lang" "$lines"
done

# -----------------------------
# Sort and print groups
# -----------------------------
declare -a group_list
for group in Database Backend Frontend Media; do
    var_name="${group,,}_lines"
    lines="${!var_name:-0}"
    percent=$(percentage "$lines")
    group_list+=("$percent|$group|$lines")
done

IFS=$'\n' sorted_groups=($(sort -t '|' -k1 -nr <<<"${group_list[*]}"))
unset IFS

echo
for entry in "${sorted_groups[@]}"; do
    IFS='|' read -r percent group lines <<< "$entry"
    print_group "$group" "$lines"
done
