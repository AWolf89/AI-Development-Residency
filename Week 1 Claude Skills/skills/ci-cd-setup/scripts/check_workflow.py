#!/usr/bin/env python3
"""Check GitHub Actions workflow files against the skill's rules.

Checks each .yml/.yaml file: every 'uses:' pinned to a 40-character commit SHA with a
version comment (local ./ actions excepted); a top-level 'permissions:' block; CI
workflows trigger on push and pull_request; deploy workflows trigger only on
workflow_dispatch.

Usage: python3 check_workflow.py <workflow-file-or-folder>
Exit codes: 0 = all pass, 1 = problems found, 2 = bad input.
"""
import os
import re
import sys


def triggers(text):
    m = re.search(r"^on:\s*(.*?)(?=^\S)", text + "\nEND", re.M | re.S)
    if not m:
        return set()
    block = m.group(1)
    inline = re.findall(r"[\w-]+", block.split("\n")[0])
    nested = re.findall(r"^\s{2}([\w-]+):", block, re.M)
    return set(inline + nested)


def check(path, text):
    problems = []
    for i, line in enumerate(text.splitlines(), 1):
        m = re.search(r"uses:\s*([^\s#]+)(\s*#\s*(\S+))?", line)
        if not m or m.group(1).startswith("./"):
            continue
        ref = m.group(1).split("@")[-1] if "@" in m.group(1) else ""
        if not re.fullmatch(r"[0-9a-f]{40}", ref):
            problems.append(f"{path}:{i}: '{m.group(1)}' not pinned to a full commit SHA")
        elif not m.group(3):
            problems.append(f"{path}:{i}: SHA pin missing a version comment (# vX.Y.Z)")
    if not re.search(r"^permissions:", text, re.M):
        problems.append(f"{path}: missing top-level 'permissions:' block")
    t = triggers(text)
    if "deploy" in os.path.basename(path).lower():
        if t != {"workflow_dispatch"}:
            problems.append(f"{path}: deploy must trigger only on workflow_dispatch (found: {sorted(t)})")
    elif not {"push", "pull_request"} <= t:
        problems.append(f"{path}: CI must trigger on push and pull_request (found: {sorted(t)})")
    return problems


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    target = sys.argv[1]
    if os.path.isdir(target):
        paths = [os.path.join(target, f) for f in sorted(os.listdir(target)) if f.endswith((".yml", ".yaml"))]
    elif os.path.isfile(target):
        paths = [target]
    else:
        print(f"ERROR: {target} not found", file=sys.stderr)
        sys.exit(2)
    if not paths:
        print(f"ERROR: no workflow files in {target}", file=sys.stderr)
        sys.exit(2)
    problems = []
    for p in paths:
        problems += check(p, open(p, encoding="utf-8").read())
    for pr in problems:
        print(f"FAIL: {pr}")
    if problems:
        sys.exit(1)
    print(f"PASS: {len(paths)} workflow file(s) meet the rules")


if __name__ == "__main__":
    main()
