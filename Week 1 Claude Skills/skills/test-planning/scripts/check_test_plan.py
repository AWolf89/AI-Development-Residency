#!/usr/bin/env python3
"""Check a test plan has every required section, at least one critical path,
and at least one Kanban card.

Usage: python3 check_test_plan.py docs/test-plan/<name>.md
Exit codes: 0 = pass, 1 = problems found, 2 = bad input (missing/unreadable file).
"""
import re
import sys

REQUIRED = [
    "Project choices",
    "Critical paths",
    "Unit tests",
    "Integration tests",
    "End-to-end tests",
    "Edge cases and errors",
    "Kanban cards",
]
NEEDS_BULLETS = ["Critical paths", "Unit tests", "Kanban cards"]


def section(text, name):
    m = re.search(rf"^##\s+{re.escape(name)}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def check(text):
    problems = []
    headings = [h.strip() for h in re.findall(r"^##\s+(.+)$", text, re.M)]
    for name in REQUIRED:
        if name not in headings:
            problems.append(f"Missing section: '## {name}'")
    found = [h for h in headings if h in REQUIRED]
    if not problems and found != REQUIRED:
        problems.append("Sections are out of order; expected: " + ", ".join(REQUIRED))
    for name in NEEDS_BULLETS:
        body = section(text, name)
        if body is not None and not re.search(r"^\s*[-*]\s+\S", body, re.M):
            problems.append(f"Section '{name}' has no items")
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
    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        sys.exit(1)
    print("PASS: test plan has all sections, critical paths, and Kanban cards")


if __name__ == "__main__":
    main()
