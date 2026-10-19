#!/usr/bin/env python3
"""Validate branch names and Conventional Commit messages.

Usage:
  python3 check_names.py branch <name>
  python3 check_names.py commit "<message>"
Exit codes: 0 = valid, 1 = invalid (reasons printed), 2 = bad usage.
"""
import re
import sys

TYPES = ["feat", "fix", "docs", "test", "refactor", "chore", "ci", "perf", "style", "build"]
T = "|".join(TYPES)


def check_branch(name):
    errors = []
    if name in ("main", "master"):
        return ["never work directly on main"]
    if not re.fullmatch(rf"({T})/[a-z0-9]+(-[a-z0-9]+)*", name):
        errors.append(f"must be type/short-description, lowercase-hyphenated; types: {', '.join(TYPES)}")
    if len(name) > 50:
        errors.append(f"too long ({len(name)} chars, max 50)")
    return errors


def check_commit(msg):
    errors = []
    first = msg.splitlines()[0] if msg else ""
    m = re.fullmatch(rf"({T})(\([a-z0-9-]+\))?(!)?: (.+)", first)
    if not m:
        return [f"first line must be 'type(scope): description'; types: {', '.join(TYPES)}"]
    desc = m.group(4)
    if len(first) > 72:
        errors.append(f"first line too long ({len(first)} chars, max 72)")
    if desc[0].isupper():
        errors.append("description should start lowercase")
    if desc.endswith("."):
        errors.append("no trailing period")
    if re.match(r"\w+(ed|ing)\b", desc):
        errors.append("use imperative mood ('add', not 'added'/'adding')")
    lines = msg.splitlines()
    if len(lines) > 1 and lines[1].strip():
        errors.append("leave a blank line between the first line and the body")
    return errors


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("branch", "commit"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help") else 2)
    kind, value = sys.argv[1], sys.argv[2]
    errors = check_branch(value) if kind == "branch" else check_commit(value)
    for e in errors:
        print(f"FAIL: {e}")
    if errors:
        sys.exit(1)
    print(f"PASS: valid {kind}")


if __name__ == "__main__":
    main()
