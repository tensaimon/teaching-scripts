#!/usr/bin/env python3
"""
student-lists.py — reformat a student list and optionally assign groups.

Usage:
    python student-lists.py input.txt
    python student-lists.py input.txt 3

Output is written to INPUTFILENAME_output.txt (tab-separated, so it can be
pasted into a spreadsheet with each field in its own cell).
"""

import os
import sys


def parse_students(path):
    """Read the file and return a list of (number, kanji_name, romaji_name) tuples.
    Each student occupies two lines: 'ID kanji-name' then 'romaji-name faculty dept grade sex'.
    The romaji name is all leading ASCII tokens on line 2, up to the first Japanese text."""
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    if len(lines) % 2 != 0:
        sys.exit(f"Warning: {path} has an odd number of non-empty lines "
                 f"({len(lines)}). Check for a missing or extra line — "
                 "students must come in two-line pairs.")

    students = []
    for i in range(0, len(lines), 2):
        id_line = lines[i].split()
        romaji_line = lines[i + 1].split()

        # Romaji name = all leading tokens that contain no Japanese characters
        romaji_tokens = []
        for tok in romaji_line:
            if any(ord(ch) > 0x3000 for ch in tok):  # first Japanese/CJK token ends the name
                break
            romaji_tokens.append(tok)

        students.append((
            id_line[0],                       # student ID
            " ".join(id_line[1:]),            # kanji name (may be 2+ tokens)
            " ".join(romaji_tokens),          # full romaji name
        ))
    return students


def assign_groups(n_students, n_groups):
    """Return a list of group numbers, sizes as equal as possible,
    with earlier groups getting the extra student (e.g. 25 / 3 groups -> 7, 6, 6)."""
    sizes = [n_students // n_groups] * n_groups
    for i in range(n_students % n_groups):
        sizes[i] += 1
    groups = []
    for g, size in enumerate(sizes, start=1):
        groups.extend([g] * size)
    return groups


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python student-lists.py input.txt [num_groups]")

    input_path = sys.argv[1]
    students = parse_students(input_path)

    # Optional second arg: number of groups
    groups = None
    if len(sys.argv) >= 3:
        n = int(sys.argv[2])
        if n <= 0:
            sys.exit("Number of groups must be a positive integer.")
        groups = assign_groups(len(students), n)

    # Output file: INPUTFILENAME_output.txt
    base = os.path.splitext(input_path)[0]
    output_path = base + "_output.txt"

    with open(output_path, "w", encoding="utf-8") as out:
        for i, (num, kanji, romaji) in enumerate(students):
            g = groups[i] if groups else ""
            out.write(f"{g}\t{num}\t{kanji}\t{romaji}\n")

    print(f"Wrote {len(students)} students to {output_path}")


if __name__ == "__main__":
    main()
