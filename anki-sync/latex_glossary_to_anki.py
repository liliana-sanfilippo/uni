#!/usr/bin/env python3

import re
import csv
import argparse
from pathlib import Path
from collections import defaultdict


def extract_brace_content(text, start):
    """Liest den Inhalt einer geschweiften Klammer inkl. verschachtelter Klammern."""
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
        m = re.search(r'([a-zA-Z]+)\s*=\s*(\{)?', body[pos:])
        if not m:
            break

        key = m.group(1)
        has_braces = m.group(2) == "{"

        if has_braces:
            start = pos + m.end()
            value, end = extract_brace_content(body, start)
            fields[key] = value.strip()
            pos = end + 1
        else:
            start = pos + m.end()
            end = body.find(",", start)
            if end == -1:
                end = len(body)

            fields[key] = body[start:end].strip()
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


def resolve_glossary_refs(text, glossary):
    """Ersetzt Glossarverweise durch den Namen des Glossarbegriffs."""

    def repl(match):
        command = match.group(1)
        key = match.group(2)

        name = glossary.get(key, key)

        if command.startswith("G"):
            name = name[:1].upper() + name[1:]

        return name

    pattern = r'\\(gls|Gls|glspl|Glspl)\{([^}]+)\}'
    return re.sub(pattern, repl, text)


def clean_latex(text):
    """Entfernt einfache LaTeX-Formatierung."""

    # Zeilenumbrüche entfernen
    text = re.sub(r"\s+", " ", text)

    # Formatierungsbefehle entfernen, Inhalt behalten
    text = re.sub(
        r'\\(?:textbf|textit|emph|textrm|texttt|underline)\{([^}]*)\}',
        r'\1',
        text
    )

    # Geschütztes Leerzeichen
    text = text.replace("~", " ")

    # Mehrere Leerzeichen
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def main():
    parser = argparse.ArgumentParser(
        description="LaTeX-Glossar in Anki-CSV-Dateien umwandeln."
    )

    parser.add_argument("input", help="Glossar (.tex)")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="anki_csv",
        help="Ausgabeverzeichnis"
    )

    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        tex = f.read()

    entries = parse_glossary(tex)

    # key -> Name
    glossary = {
        entry["key"]: entry["name"]
        for entry in entries
    }

    # Referenzen auflösen
    for entry in entries:
        entry["description"] = resolve_glossary_refs(
            entry["description"],
            glossary
        )
        entry["description"] = clean_latex(
            entry["description"]
        )

    groups = defaultdict(list)

    for entry in entries:
        groups[entry["type"]].append(entry)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename_map = {
        "defi": "definition.csv",
        "begriff": "begriff.csv",
        "satz": "satz.csv",
        "formel": "formel.csv",
        "frage": "fragen.csv",
        "algorithmus": "algorithmus.csv",
    }

    total = 0

    for typ, items in sorted(groups.items()):
        filename = filename_map.get(typ, f"{typ}.csv")

        with open(output_dir / filename,
                  "w",
                  newline="",
                  encoding="utf-8") as f:

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