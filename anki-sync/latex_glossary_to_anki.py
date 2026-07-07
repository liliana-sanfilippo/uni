#!/usr/bin/env python3

import re
import csv
import argparse
from pathlib import Path
from collections import defaultdict



def extract_brace_content(text, start):
    """Liest den Inhalt einer geschweiften Klammer inklusive verschachtelter Klammern."""
    depth = 1
    i = start
    content = ""

    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return content, i

        content += text[i]
        i += 1

    raise ValueError("Unmatched braces")


def parse_fields(body):
    fields = {}
    pos = 0

    while pos < len(body):
        m = re.search(r'([a-zA-Z]+)\s*=\s*\{', body[pos:])
        if not m:
            break

        key = m.group(1)
        start = pos + m.end()
        value, end = extract_brace_content(body, start)

        fields[key] = value.strip()
        pos = end + 1

    return fields


def parse_glossary(tex):
    entries = []

    pattern = r'\\newglossaryentry\s*\{([^}]*)\}\s*\{'
    pos = 0

    while True:
        m = re.search(pattern, tex[pos:])
        if not m:
            break

        key = m.group(1)

        start = pos + m.end()
        body, end = extract_brace_content(tex, start)

        fields = parse_fields(body)

        entries.append({
            "key": key,
            "name": fields.get("name", key),
            "description": fields.get("description", ""),
            "type": fields.get("type", "default")
        })

        pos = end + 1

    return entries


def main():
    parser = argparse.ArgumentParser(
        description="Konvertiert ein LaTeX-Glossar in mehrere Anki-CSV-Dateien."
    )
    parser.add_argument("input", help="LaTeX-Datei (.tex)")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="anki_csv",
        help="Ausgabeverzeichnis (Standard: anki_csv)"
    )

    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        tex = f.read()

    entries = parse_glossary(tex)

    groups = defaultdict(list)

    for entry in entries:
        groups[entry["type"]].append(entry)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Optionale Zuordnung von Typen zu Dateinamen
    filename_map = {
        "defi": "definition.csv",
        "begriff": "begriff.csv",
        "algorithmus": "algorithmus.csv",
        "satz": "satz.csv",
        "formel": "formel.csv",
    }

    total = 0

    for typ, items in sorted(groups.items()):
        filename = filename_map.get(typ, f"{typ}.csv")
        filepath = output_dir / filename

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            for item in items:
                writer.writerow([
                    item["name"],
                    item["description"]
                ])

        print(f"{filename:<20} {len(items):>4} Einträge")
        total += len(items)

    print(f"\nInsgesamt exportiert: {total} Einträge")


if __name__ == "__main__":
    main()