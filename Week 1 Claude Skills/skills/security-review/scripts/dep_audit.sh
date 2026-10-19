#!/usr/bin/env bash
# Run dependency vulnerability scans for a repo (read-only).
# Usage: bash dep_audit.sh <repo-path>
# Python: pip-audit on requirements*.txt (or the current environment if only pyproject).
# JavaScript: npm audit where package.json exists.
# Exit codes: 0 = no known vulnerabilities, 1 = vulnerabilities found,
#             2 = bad input, 3 = a needed tool is missing.
set -uo pipefail
if [[ $# -ne 1 || "$1" == "-h" || "$1" == "--help" ]]; then sed -n '2,8p' "$0"; [[ $# -eq 1 ]] && exit 0 || exit 2; fi
repo="$1"; [[ -d "$repo" ]] || { echo "ERROR: $repo not found" >&2; exit 2; }
found=0; missing=0; scanned=0

mapfile -t reqs < <(find "$repo" -name 'requirements*.txt' -not -path '*/node_modules/*' -not -path '*/.venv/*' 2>/dev/null)
if (( ${#reqs[@]} )) || [[ -f "$repo/pyproject.toml" ]]; then
  if command -v pip-audit >/dev/null 2>&1; then
    if (( ${#reqs[@]} )); then
      for r in "${reqs[@]}"; do
        echo "== pip-audit: $r"; scanned=1
        pip-audit -r "$r" || found=1
      done
    else
      echo "== pip-audit: current environment (pyproject.toml only; install the project first)"; scanned=1
      pip-audit || found=1
    fi
  else
    echo "MISSING: pip-audit (see references/tools.md)" >&2; missing=1
  fi
fi

mapfile -t pkgs < <(find "$repo" -name package.json -not -path '*/node_modules/*' 2>/dev/null)
for p in "${pkgs[@]}"; do
  d=$(dirname "$p")
  if command -v npm >/dev/null 2>&1; then
    echo "== npm audit: $d"; scanned=1
    if [[ -f "$d/package-lock.json" ]]; then (cd "$d" && npm audit) || found=1
    else echo "WARN: no package-lock.json in $d; npm audit needs one (run npm install)" >&2; found=1; fi
  else
    echo "MISSING: npm" >&2; missing=1
  fi
done

(( scanned == 0 && missing == 0 )) && echo "No Python or JavaScript manifests found."
(( missing )) && exit 3
(( found )) && { echo "RESULT: issues found - review above"; exit 1; }
echo "RESULT: no known vulnerabilities"; exit 0
