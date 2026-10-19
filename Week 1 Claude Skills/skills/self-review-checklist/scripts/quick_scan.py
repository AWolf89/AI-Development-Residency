#!/usr/bin/env python3
"""Flag mechanical self-review issues in Python and JavaScript/TypeScript files.

Usage: python3 quick_scan.py <file-or-folder> [more ...]
Each hit is a lead to confirm by reading, not an automatic fail.
Exit codes: 0 = no hits, 1 = hits found, 2 = bad input (path missing).
"""
import os
import re
import sys

EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
SKIP_DIRS = {"node_modules", ".git", "venv", ".venv", "dist", "build", "__pycache__"}
RULES = [
    (r"^\s*print\(", {".py"}, "print() used - use logging"),
    (r"console\.log\(", None, "console.log used - use a logger"),
    (r"^\s*except\s*:", {".py"}, "bare except - catch a specific error"),
    (r"except\s+Exception\s*(as\s+\w+)?\s*:\s*pass", {".py"}, "error swallowed silently"),
    (r"catch\s*\([^)]*\)\s*\{\s*\}", None, "empty catch block - error swallowed"),
    (r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]", None,
     "possible hardcoded secret"),
]


def files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for n in names:
                    yield os.path.join(root, n)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if args else 2)
    missing = [p for p in args if not os.path.exists(p)]
    if missing:
        print("ERROR: not found: " + ", ".join(missing), file=sys.stderr)
        sys.exit(2)
    hits = 0
    for path in files(args):
        ext = os.path.splitext(path)[1]
        if ext not in EXTS:
            continue
        try:
            lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        except OSError as e:
            print(f"WARN: cannot read {path}: {e}", file=sys.stderr)
            continue
        for i, line in enumerate(lines, 1):
            for pattern, only, msg in RULES:
                if (only is None or ext in only) and re.search(pattern, line):
                    print(f"{path}:{i}: {msg}")
                    hits += 1
    print(f"{hits} hit(s)")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
