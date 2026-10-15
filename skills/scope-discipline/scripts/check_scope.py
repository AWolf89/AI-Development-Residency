#!/usr/bin/env python3
"""Compare what was actually changed against the declared scope.

Memory is unreliable for this: a file opened early and edited casually is easy to forget,
and the reviewer is the one who pays for it. This check is mechanical so it gives the same
answer every time.

Reports:
  * files changed that were not declared in scope
  * files changed that were explicitly declared out of scope (an error, not a warning)
  * dependency, lockfile, CI, and config changes that were not authorized
  * diffs whose shape suggests reformatting or rewriting rather than a targeted edit
  * declared files that were never touched (often a sign the task is incomplete)

Usage:
    python3 check_scope.py scope.json                      # reads `git diff` in cwd
    python3 check_scope.py scope.json --staged             # staged changes only
    python3 check_scope.py scope.json --files a.py b.py    # no git available
    python3 check_scope.py scope.json --json

Exit codes: 0 clean · 1 scope violations found · 2 unreadable input
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

SENSITIVE_PATTERNS = {
    "dependency": [
        "requirements*.txt", "pyproject.toml", "poetry.lock", "Pipfile*", "setup.py",
        "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        "go.mod", "go.sum", "Gemfile*", "Cargo.toml", "Cargo.lock", "*.csproj",
    ],
    "config/CI": [
        ".github/**", ".gitlab-ci.yml", "Dockerfile*", "docker-compose*",
        "*.tf", "*.tfvars", "Makefile", ".pre-commit-config.yaml",
        ".eslintrc*", ".prettierrc*", "setup.cfg", "tox.ini", ".editorconfig",
        "*.env*", "**/settings.py", "**/config/**",
    ],
}

# A change that deletes and re-adds most of a file usually means a reformat or rewrite.
REFORMAT_MIN_LINES = 40
REFORMAT_RATIO = 0.75


def run_git(args: list[str]) -> str | None:
    try:
        out = subprocess.run(["git", *args], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout


def changed_files_from_git(staged: bool) -> list[str] | None:
    args = ["diff", "--name-only"] + (["--cached"] if staged else [])
    out = run_git(args)
    if out is None:
        return None
    files = [l.strip() for l in out.splitlines() if l.strip()]
    if not staged:
        untracked = run_git(["ls-files", "--others", "--exclude-standard"]) or ""
        files += [l.strip() for l in untracked.splitlines() if l.strip()]
    return sorted(set(files))


def diff_stats(path: str, staged: bool) -> tuple[int, int] | None:
    args = ["diff", "--numstat"] + (["--cached"] if staged else []) + ["--", path]
    out = run_git(args)
    if not out:
        return None
    parts = out.split()
    if len(parts) < 2 or not parts[0].isdigit() or not parts[1].isdigit():
        return None
    return int(parts[0]), int(parts[1])


def matches(path: str, patterns: list[str]) -> bool:
    p = path.replace("\\", "/")
    for pat in patterns:
        pat = pat.replace("\\", "/")
        if fnmatch.fnmatch(p, pat) or fnmatch.fnmatch(Path(p).name, pat):
            return True
        if "**" in pat and fnmatch.fnmatch(p, pat.replace("**", "*")):
            return True
        if pat.endswith("/") and p.startswith(pat):
            return True
    return False


def load_scope(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("scope file must be a JSON object")
    data.setdefault("in_scope", [])
    data.setdefault("in_scope_globs", [])
    data.setdefault("explicitly_out_of_scope", [])
    data.setdefault("widened", [])
    return data


def check(scope: dict, changed: list[str], staged: bool) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []

    declared = [str(f) for f in scope["in_scope"]]
    globs = [str(g) for g in scope["in_scope_globs"]]
    widened = [str(w.get("path", "")) for w in scope.get("widened", []) if isinstance(w, dict)]
    allowed = set(declared) | set(widened)

    # "explicitly_out_of_scope" entries may carry an explanation after an em dash.
    banned = [str(x).split("—")[0].strip() for x in scope["explicitly_out_of_scope"]]

    in_scope_hits: set[str] = set()

    for f in changed:
        if f in allowed or matches(f, globs):
            in_scope_hits.add(f)
            continue

        if matches(f, [b for b in banned if b]):
            errors.append(f"{f}: changed, but declared explicitly OUT of scope. "
                          "Revert it, or get the boundary widened on the record.")
            continue

        kinds = [kind for kind, pats in SENSITIVE_PATTERNS.items() if matches(f, pats)]
        if kinds:
            flag = ("allow_dependency_changes" if "dependency" in kinds
                    else "allow_config_changes")
            if not scope.get(flag, False):
                errors.append(f"{f}: {kinds[0]} file changed without authorization "
                              f"({flag} is false). These reach further than one ticket.")
                continue

        errors.append(f"{f}: changed but never declared in scope. "
                      "Either it belongs in the declaration, or it should not have been touched.")

    for f in declared:
        if f not in changed:
            warnings.append(f"{f}: declared in scope but not changed. "
                            "Fine if it turned out unnecessary — worth confirming the task is complete.")

    if staged is not None:
        for f in sorted(in_scope_hits):
            stats = diff_stats(f, staged)
            if not stats:
                continue
            added, removed = stats
            total = added + removed
            if total >= REFORMAT_MIN_LINES and removed >= REFORMAT_RATIO * added:
                warnings.append(
                    f"{f}: {added} added / {removed} removed — the shape of a reformat or "
                    "rewrite rather than a targeted edit. Check for drive-by changes that "
                    "will bury the real one in review.")

    if not scope.get("observations"):
        warnings.append("No observations recorded. Noticing nothing at all is unusual; if "
                        "something was skipped deliberately, it is worth writing down.")

    summary = {
        "changed_files": len(changed),
        "in_scope": len(in_scope_hits),
        "violations": len(errors),
        "observations_recorded": len(scope.get("observations", []) or []),
    }
    return errors, warnings, summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scope", help="Path to scope.json")
    ap.add_argument("--files", nargs="*", help="Changed files, when git is unavailable")
    ap.add_argument("--staged", action="store_true", help="Check staged changes only")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    scope_path = Path(args.scope)
    if not scope_path.is_file():
        print(f"ERROR: no such file: {scope_path}", file=sys.stderr)
        return 2
    try:
        scope = load_scope(scope_path)
    except Exception as exc:
        print(f"ERROR: could not read {scope_path}: {exc}", file=sys.stderr)
        return 2

    use_git = args.files is None
    if use_git:
        changed = changed_files_from_git(args.staged)
        if changed is None:
            print("ERROR: no git repository detected (or git failed). "
                  "Pass the changed files with --files instead.", file=sys.stderr)
            return 2
    else:
        changed = sorted(set(args.files))

    errors, warnings, summary = check(scope, changed, args.staged if use_git else None)

    if args.json:
        print(json.dumps({"summary": summary, "errors": errors, "warnings": warnings}, indent=2))
    else:
        print(f"{summary['changed_files']} file(s) changed · {summary['in_scope']} in scope · "
              f"{summary['violations']} violation(s) · "
              f"{summary['observations_recorded']} observation(s) recorded\n")
        for e in errors:
            print(f"VIOLATION  {e}")
        for w in warnings:
            print(f"WARNING    {w}")
        if not errors and not warnings:
            print("PASS  every change falls inside the declared boundary.")
        print(f"\n{len(errors)} violation(s), {len(warnings)} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
