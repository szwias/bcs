#!/bin/bash
# Script to count lines in different file types excluding certain directories

tracked=false
if [[ $1 == "--tracked" ]]; then
  tracked=true
fi

backup

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/bcs/" || exit 1

if $tracked; then
  plpgsql_lines=$(find . -name '*.sql' \
    ! -path '*/backups/*' \
    ! -path '*/baza/baza*.sql' \
    -exec cat {} + | wc -l)

  json_lines=$(find . -name '*.json' \
    ! -path '*/media/*' \
    -exec cat {} + | wc -l)
else
  plpgsql_lines=$(find . -name '*.sql' \
    ! -path '*/backups/*' \
    -exec cat {} + | wc -l)

  json_lines=$(find . -name '*.json' -exec cat {} + | wc -l)
fi

python_lines=$(find . -name '*.py' \
  ! -path '*/migrations/*' \
  -exec cat {} + | wc -l)

bash_lines=$(find . -name '*.bash' \
  -exec cat {} + | wc -l)

html_lines=$(find . -name '*.html' -exec cat {} + | wc -l)

css_lines=$(find . -name '*.css' \
  ! -path "*/staticfiles/*" \
  -exec cat {} + | wc -l)

scss_lines=$(find . -name '*.scss' \
  ! -path "*/staticfiles/*" \
  -exec cat {} + | wc -l)

js_lines=$(find . -name '*.js' \
  ! -path "*/staticfiles/*" \
  -exec cat {} + | wc -l)

# Totals
backend_lines=$((python_lines))
database_lines=$((plpgsql_lines))
management_lines=$((bash_lines))
if $tracked; then
  frontend_lines=$((html_lines + scss_lines + js_lines))
else
  frontend_lines=$((html_lines + scss_lines + css_lines + js_lines))
fi
media_lines=$((json_lines))
total_lines=$((backend_lines + management_lines + database_lines + frontend_lines + media_lines))

echo
echo "Total lines: $total_lines"

# Colors
START="\033[38;5;"
RESET="\033[0m"

declare -A hex_lang_colors=(
  ["PLpgSQL"]="#E38C00"
  ["Python"]="#3572A5"
  ["Bash"]="#89E051"
  ["HTML"]="#E34C26"
  ["CSS"]="#563D7C"
  ["SCSS"]="#C6538C"
  ["JS"]="#F1E05A"
  ["JSON"]="#292929"
)

declare -A lang_colors=(
  ["PLpgSQL"]=172
  ["Python"]=25
  ["Bash"]=113
  ["HTML"]=166
  ["CSS"]=54
  ["SCSS"]=168
  ["JS"]=221
  ["JSON"]=102
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
  local color="${START}${lang_colors[$group]}m"
  printf "$color%-10s | %7d | %6s%%${RESET}\n" "$group" "$lines" "$percent"
}

# -----------------------------
# Sort and print languages
# -----------------------------
if $tracked; then
  langs=(PLpgSQL Python Bash HTML SCSS JS)
else
  langs=(PLpgSQL Python Bash HTML SCSS CSS JS JSON)
fi

declare -a lang_list
for lang in "${langs[@]}"; do
  lines_var="${lang,,}_lines"
  lines="${!lines_var:-0}"
  percent=$(percentage "$lines")
  lang_list+=("$percent|$lang|$lines")
done

IFS=$'\n' sorted_langs=($(sort -t '|' -k1 -nr <<<"${lang_list[*]}"))
unset IFS

echo
for entry in "${sorted_langs[@]}"; do
  IFS='|' read -r percent lang lines <<<"$entry"
  print_colored "$lang" "$lines"
done

# -----------------------------
# Sort and print groups
# -----------------------------
declare -a group_list
if $tracked; then
  declare -A group_langs=(
    ["Database"]="PLpgSQL"
    ["Backend"]="Python"
    ["Frontend"]="HTML SCSS JS"
    ["Management"]="Bash"
  )
else
  declare -A group_langs=(
    ["Database"]="PLpgSQL"
    ["Backend"]="Python"
    ["Frontend"]="HTML SCSS CSS JS"
    ["Media"]="JSON"
    ["Management"]="Bash"
  )
fi

get_group_color() {
  local type=$1
  local group=$2
  local max_lang=""
  local max_lines=0
  for lang in ${group_langs[$group]}; do
    local lines_var="${lang,,}_lines"
    local lines="${!lines_var:-0}"
    if ((lines > max_lines)); then
      max_lines=$lines
      max_lang=$lang
    fi
  done
  if [[ $type == "tput" ]]; then
    echo "${lang_colors[$max_lang]}"
  elif [[ $type == "hex" ]]; then
    echo "${hex_lang_colors[$max_lang]}"
  fi
}

if $tracked; then
  groups=(Database Backend Frontend Management)
else
  groups=(Database Backend Frontend Media Management)
fi

for group in "${groups[@]}"; do
  var_name="${group,,}_lines"
  lines="${!var_name:-0}"
  percent=$(percentage "$lines")

  # Pick color dynamically based on dominant language
  color_code=$(get_group_color "tput" "$group")
  group_list+=("$percent|$group|$lines|$color_code")
done

IFS=$'\n' sorted_groups=($(sort -t '|' -k1 -nr <<<"${group_list[*]}"))
unset IFS

echo
for entry in "${sorted_groups[@]}"; do
  IFS='|' read -r percent group lines color_code <<<"$entry"
  color="${START}${color_code}m"
  printf "$color%-10s | %7d | %6s%%${RESET}\n" "$group" "$lines" "$percent"
done

# -----------------------------
# Write to file if --tracked
# -----------------------------
if $tracked; then
  output_file="../stats/tcount/tdata.txt"
else
  output_file="../stats/count/data.txt"
fi
: >"$output_file" # truncate file

echo "# Languages" >>"$output_file"
for entry in "${sorted_langs[@]}"; do
  IFS='|' read -r percent lang lines <<<"$entry"
  echo "$lang,$lines,${hex_lang_colors[$lang]}" >>"$output_file"
done

echo >>"$output_file"

echo "# Groups" >>"$output_file"
for entry in "${sorted_groups[@]}"; do
  IFS='|' read -r percent group lines color_code <<<"$entry"
  echo "$group,$lines,$(get_group_color "hex" "$group")" >>"$output_file"
done
