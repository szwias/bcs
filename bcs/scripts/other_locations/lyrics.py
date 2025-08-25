#!/usr/bin/env python
import sys
import os
import re

if len(sys.argv) < 5:
    print(f"Usage: {sys.argv[0]} <scope> <mode> <input> <output>")
    sys.exit(0)
elif "--help" in sys.argv or "-h" in sys.argv:
    print(
        """
        Song Lyrics to JSON Converter

        Usage:
            python lyrics_converter.py <scope> <mode> <input> <output>

        Arguments:
            scope          What to process:
                              - "file" : process a single file
                              - "dir"  : process all files in a directory

            mode           How to interpret the input file(s):
                              - "cols"   : first half of lines are chords, second half are lyrics
                              - "points" : first line contains comma-separated point indices for sections

            input          Path to the input file or input directory depending on scope
                              - For "file" scope, provide the filename relative to /home/szymon/Downloads/Śpiewnik/
                              - For "dir" scope, provide the path to a directory containing text files

            output         Path to the output file or output directory depending on scope
                              - For "file" scope, the output JSON filename (without "_1.json")
                              - For "dir" scope, the directory where converted JSON files will be written

        Description:
            This script reads song lyrics text files, optionally with chords, and converts them
            into JSON format suitable for use in a songbook application. Each line becomes a JSON
            object with the "tekst" (lyrics) field and an array of chords ("chwyty").

            Chords are parsed to respect parentheses, e.g.:
                ea(A7)  -> ["e", "a", "(A7)"]

        Examples:
            # Convert a single file
            python lyrics_converter.py file cols "Gaudeamus.txt" "gaudeamus"

            # Convert all files in a directory
            python lyrics_converter.py dir points "/home/user/input_songs" "/home/user/output_json"

        Notes:
            - Ensure that input files are UTF-8 encoded.
            - The script automatically creates output directories if they do not exist.
            - Parentheses in chords are preserved.
        """
    )
    sys.exit(1)

scope = sys.argv[1]
mode = sys.argv[2]


def parse_chords(line: str):
    # Capture either parenthesized chunks (...) or single chord symbols
    tokens = re.findall(r"\([^)]*\)|[A-Ga-g][#b]?[0-9]*", line)
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
    with open(in_file, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]

        if mode == "cols":
            if len(lines) % 2:
                result.append(
                    '  {"tekst": "' + lines[0] + '",\n  "chords": []},\n'
                )
                lines = lines[1:]

            half = len(lines) // 2
            [
                result.append(build_object(lines[half + i], lines[i]))
                for i in range(half)
            ]
            result[-1] = result[-1][:-2] + "\n"

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
                        result.append(build_object(lines[i], lines[i]))
                    elif (i - point) % 2 == 0:
                        result.append(build_object(lines[i + 1], lines[i]))
                    continue
                else:
                    result.append(build_object(lines[i], ""))

            result[-1] = result[-1][:-2] + "\n"

    with open(out_file, "w", encoding="utf-8") as out:
        out.write("[\n")
        out.writelines(result)
        out.write("]")


if scope == "dir":

    input_dir = sys.argv[3]
    output_dir = sys.argv[4]

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)

        # Skip if it's not a regular file (ignore subdirectories, symlinks, etc.)
        if not os.path.isfile(input_file):
            continue

        # Use the same base name, but with .json extension
        base, _ = os.path.splitext(filename)
        output_file = os.path.join(output_dir, base + "_1.json")

        logic(input_file, output_file)

elif scope == "file":

    input_file = "/home/szymon/Downloads/Śpiewnik/" + sys.argv[3]
    output_file = (
        "/home/szymon/Desktop/BCS/Piosenki/" + sys.argv[4] + "_1.json"
    )

    logic(input_file, output_file)
