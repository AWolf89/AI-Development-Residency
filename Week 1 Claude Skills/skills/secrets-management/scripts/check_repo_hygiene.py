#!/usr/bin/env python3
"""Check a repo's secrets hygiene (read-only).

Checks: .gitignore ignores .env files; no .env file is tracked by git; .env.example is
present when a .env exists; docker-compose files have no inline secret-like values;
the gitleaks pre-commit hook is installed.

Usage: python3 check_repo_hygiene.py <repo-path>
Exit codes: 0 = all pass, 1 = problems found, 2 = bad input (not a git repo).
"""
import glob
import os
import re
import subprocess
import sys

SECRET_NAME = re.compile(r"(?i)(key|secret|token|password|passwd|pwd)")


def tracked_files(repo):
    out = subprocess.run(["git", "-C", repo, "ls-files"], capture_output=True, text=True)
    return out.stdout.splitlines() if out.returncode == 0 else []


def check(repo):
    results = []
    gi = os.path.join(repo, ".gitignore")
    text = open(gi, encoding="utf-8").read() if os.path.exists(gi) else ""
    lines = [l.strip() for l in text.splitlines()]
    results.append((".gitignore ignores .env", ".env" in lines or ".env*" in lines))
    tracked = tracked_files(repo)
    leaked = [f for f in tracked if re.search(r"(^|/)\.env($|\.)", f) and not f.endswith(".env.example")]
    results.append(("no .env file tracked by git" + (f" (found: {', '.join(leaked)})" if leaked else ""), not leaked))
    has_env = os.path.exists(os.path.join(repo, ".env"))
    has_example = os.path.exists(os.path.join(repo, ".env.example"))
    results.append((".env.example present (needed because .env exists)", has_example or not has_env))
    inline = []
    for path in glob.glob(os.path.join(repo, "**", "*compose*.y*ml"), recursive=True):
        for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
            m = re.match(r"\s*-?\s*([A-Za-z_][A-Za-z0-9_]*)\s*[=:]\s*(\S.*)$", line)
            if m and SECRET_NAME.search(m.group(1)) and not m.group(2).startswith("${"):
                inline.append(f"{os.path.relpath(path, repo)}:{i}")
    results.append(("no inline secret values in compose files" + (f" (check: {', '.join(inline)})" if inline else ""), not inline))
    hook = os.path.join(repo, ".git", "hooks", "pre-commit")
    hook_ok = os.path.exists(hook) and "gitleaks" in open(hook, encoding="utf-8", errors="replace").read()
    results.append(("gitleaks pre-commit hook installed", hook_ok))
    return results


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    repo = sys.argv[1]
    if not os.path.isdir(os.path.join(repo, ".git")):
        print(f"ERROR: {repo} is not a git repo (no .git folder)", file=sys.stderr)
        sys.exit(2)
    results = check(repo)
    for name, ok in results:
        print(("PASS" if ok else "FAIL") + f": {name}")
    sys.exit(0 if all(ok for _, ok in results) else 1)


if __name__ == "__main__":
    main()
