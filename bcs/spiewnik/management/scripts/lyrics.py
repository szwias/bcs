#!/usr/bin/env python
import os
import re
import argparse

INPUT_PATH = "/home/szymon/Desktop/BCS/Piosenki/Pre/"
OUTPUT_PATH = "/home/szymon/Desktop/BCS/Piosenki/"

description_text = """
Song Lyrics to JSON Converter

This script reads song lyrics text files, optionally with chords, and converts them
into JSON format suitable for use in a songbook application. Each line becomes a JSON
object with the "tekst" (lyrics) field and an array of chords ("chwyty").

Chords are parsed to respect parentheses, e.g.:
    ea(A7)  -> ["e", "a", "(A7)"]

The "dull" mode is for files where the first line gives the number of chord rows,
the next N lines contain chords, and the remaining lines are lyrics.
Lines starting with "REF" or blank lines are treated as separators and have no chords.

Examples:
  Convert a single file in "dull" mode:
    python lyrics_converter.py file dull "song.txt" "song_output"

  Convert a single file in "cols" mode:
    python lyrics_converter.py file cols "Gaudeamus.txt" "gaudeamus"

  Convert all files in a directory using "points" mode:
    python lyrics_converter.py dir points "/home/user/input_songs" "/home/user/output_json"

Notes:
  - Ensure that input files are UTF-8 encoded.
  - The script automatically creates output directories if they do not exist.
  - Parentheses in chords are preserved in the JSON output.
  - Double quotes are used for chords and text in JSON for proper formatting.
"""

parser = argparse.ArgumentParser(
    description=description_text,
    formatter_class=argparse.RawTextHelpFormatter,  # preserve line breaks
)

# Required positional arguments
parser.add_argument(
    "scope",
    choices=["file", "dir"],
    help="""
What to process:
- "file" : process a single file
- "dir"  : process all files in a directory""",
)
parser.add_argument(
    "mode",
    choices=["dull", "cols", "points"],
    help="""
How to interpret the input file(s):
- "dull"   : first line = number of chord rows, next N lines = chords, remaining lines = lyrics
- "cols"   : first half of lines are chords, second half are lyrics
- "points" : first line contains comma-separated point indices for sections""",
)
parser.add_argument(
    "--input",
    "-i",
    default=INPUT_PATH,
    help=f"""
Path to the input file or input directory depending on scope
- For "file" scope, provide the filename relative to {INPUT_PATH}
- For "dir" scope, provide the path to a directory containing text files""",
)
parser.add_argument(
    "--output",
    "-o",
    default=OUTPUT_PATH,
    help=f"""
Path to the output file or output directory depending on scope
- For "file" scope, the output JSON filename (without "_1.json") relative to {OUTPUT_PATH}
- For "dir" scope, the directory where converted JSON files will be written""",
)

# Optional argument
parser.add_argument(
    "--encoding", "-e", default="utf-8", help="File encoding (default utf-8)"
)

args = parser.parse_args()

scope = args.scope
mode = args.mode


def parse_chords(line: str):
    # Capture either parenthesized chunks (...) or single chord symbols
    tokens = re.findall(pattern=r"\([^)]*\)|[A-Ga-g][#b]?[0-9]*", string=line)
    return tokens


def build_object(text, chords):
    new_line = ""
    new_line += '  {"tekst": "'
    new_line += text.replace('"', '\\"')
    new_line += '",\n'
    new_line += '   "chwyty": ['
    f_chords = parse_chords(chords)
    new_line += ", ".join([f'"{ch}"' for ch in f_chords if ch != " "])
    new_line += "]},\n"
    return new_line


def logic(in_file, out_file):
    result = []
    with open(in_file, "r", encoding=args.encoding) as f:
        lines = [l.strip() for l in f.readlines()]

        if mode == "dull":
            rows = int(lines[0])
            chords = lines[1 : rows + 1]
            inside = False
            start = 0
            for i in range(rows + 1, len(lines)):
                line = lines[i]
                if not (
                    line.strip() == ""
                    or line[:3].upper() == "REF"
                    or line[0] == "("
                ):
                    if not inside:
                        inside = True
                        start = i
                    result.append(
                        build_object(text=line, chords=chords[i - start])
                    )
                else:
                    inside = False
                    result.append(build_object(text=line, chords=""))

        elif mode == "cols":
            if len(lines) % 2:
                result.append(
                    '  {"tekst": "' + lines[0] + '",\n  "chords": []},\n'
                )
                lines = lines[1:]

            half = len(lines) // 2
            [
                result.append(
                    build_object(text=lines[half + i], chords=lines[i])
                )
                for i in range(half)
            ]

        elif mode == "points":
            points = [int(num) for num in lines[0].split(",")]
            point = 0
            inside = False
            length = len(lines)

            for i in range(length):
                if i == 0:
                    continue
                if i + 1 in points:
                    inside = True
                    point = i
                if inside:
                    if lines[i].strip() == "":
                        inside = False
                        result.append(
                            build_object(text=lines[i], chords=lines[i])
                        )
                    elif (i - point) % 2 == 0:
                        result.append(
                            build_object(text=lines[i + 1], chords=lines[i])
                        )
                    continue
                else:
                    result.append(build_object(text=lines[i], chords=""))

    result[-1] = result[-1][:-2] + "\n"

    with open(out_file, "w", encoding=args.encoding) as out:
        out.write("[\n")
        out.writelines(result)
        out.write("]")


if scope == "dir":

    input_dir = args.input
    output_dir = args.output

    # Ensure output directory exists
    os.makedirs(name=output_dir, exist_ok=True)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)

        # Skip if it's not a regular file (ignore subdirectories, symlinks, etc.)
        if not os.path.isfile(input_file):
            continue

        # Use the same base name, but with .json extension
        base, _ = os.path.splitext(filename)
        output_file = os.path.join(output_dir, base + "_1.json")

        logic(in_file=input_file, out_file=output_file)

elif scope == "file":

    input_file = INPUT_PATH + args.input
    output_file = OUTPUT_PATH + args.output + "_1.json"

    logic(in_file=input_file, out_file=output_file)
