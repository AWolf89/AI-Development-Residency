#!/usr/bin/env python3
"""Validate a self-review report table.

Checks: required items present for the checklist type, statuses valid, every row has
evidence, N/A rows give a reason, and Security basics / Scope are never N/A.

Usage: python3 check_review.py <report.md>
Exit codes: 0 = valid, 1 = problems found, 2 = bad input.
"""
import re
import sys

SHORT = ["Correctness", "Security basics", "Scope"]
FULL = ["Correctness", "Security basics", "Error handling", "Logging",
        "Readability", "Docs", "Scope", "Dependencies"]
STATUSES = {"PASS", "FIXED", "FAIL", "N/A"}
NEVER_NA = {"Security basics", "Scope"}


def check(text):
    problems = []
    m = re.search(r"^Checklist:\s*(Short|Full)\s*$", text, re.M)
    if not m:
        return ["Missing 'Checklist: Short' or 'Checklist: Full' line"]
    required = SHORT if m.group(1) == "Short" else FULL
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] not in ("Item", "") and not set(cells[0]) <= set("-: "):
            rows[cells[0]] = (cells[1], cells[2])
    for item in required:
        if item not in rows:
            problems.append(f"Missing item: {item}")
            continue
        status, evidence = rows[item]
        if status not in STATUSES:
            problems.append(f"{item}: invalid status '{status}' (use PASS, FIXED, FAIL, N/A)")
        if not evidence:
            problems.append(f"{item}: no evidence/reason given")
        if status == "N/A" and item in NEVER_NA:
            problems.append(f"{item}: can never be N/A")
    if "### Observations" not in text:
        problems.append("Missing '### Observations' section (write 'None' if empty)")
    return problems


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR: cannot read {sys.argv[1]}: {e}", file=sys.stderr)
        sys.exit(2)
    problems = check(text)
    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        sys.exit(1)
    print("PASS: review report is valid")


if __name__ == "__main__":
    main()
