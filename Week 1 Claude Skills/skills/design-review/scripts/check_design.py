#!/usr/bin/env python3
"""Check a full design document has every required section, a Mermaid diagram,
and a non-empty Kanban cards list.

Usage: python3 check_design.py docs/design/<name>.md
Exit codes: 0 = pass, 1 = problems found, 2 = bad input (missing/unreadable file).
"""
import re
import sys

REQUIRED = [
    "Problem statement",
    "Components",
    "Data flow",
    "Tech choices",
    "Security considerations",
    "Testing approach",
    "Deployment",
    "Open questions",
    "Kanban cards",
]


def check(text):
    problems = []
    headings = [h.strip() for h in re.findall(r"^##\s+(.+)$", text, re.M)]
    for name in REQUIRED:
        if name not in headings:
            problems.append(f"Missing section: '## {name}'")
    found = [h for h in headings if h in REQUIRED]
    if not problems and found != REQUIRED:
        problems.append("Sections are out of order; expected: " + ", ".join(REQUIRED))
    if "```mermaid" not in text:
        problems.append("No Mermaid diagram (a ```mermaid block) found")
    cards = re.search(r"^##\s+Kanban cards\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if cards and not re.search(r"^\s*[-*]\s+\S", cards.group(1), re.M):
        problems.append("Kanban cards section has no cards")
    return problems


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"ERROR: cannot read {sys.argv[1]}: {e}", file=sys.stderr)
        sys.exit(2)
    problems = check(text)
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        sys.exit(1)
    print("PASS: design has all sections, a Mermaid diagram, and Kanban cards")


if __name__ == "__main__":
    main()
