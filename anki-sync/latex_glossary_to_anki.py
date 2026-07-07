import re
import csv
import argparse

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
            "description": fields.get("description", "")
        })

        pos = end + 1

    return entries

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="LaTeX-Datei")
    parser.add_argument("output", help="CSV-Datei")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        tex = f.read()

    entries = parse_glossary(tex)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for e in entries:
            writer.writerow([e["name"], e["description"]])

    print(f"{len(entries)} Einträge exportiert.")

if __name__ == "__main__":
    main()