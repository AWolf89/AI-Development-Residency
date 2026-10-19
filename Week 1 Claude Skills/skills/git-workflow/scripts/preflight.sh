#!/usr/bin/env bash
# Report the repo state before starting work (read-only).
# Usage: bash preflight.sh [repo-path]
# Exit codes: 0 = on a feature branch, 1 = on main/master (create a branch first),
#             2 = not a git repo.
set -uo pipefail
repo="${1:-.}"
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then sed -n '2,5p' "$0"; exit 0; fi
git -C "$repo" rev-parse --git-dir >/dev/null 2>&1 || { echo "ERROR: $repo is not a git repo" >&2; exit 2; }
branch=$(git -C "$repo" branch --show-current)
echo "Branch: ${branch:-(detached HEAD)}"
changes=$(git -C "$repo" status --porcelain | wc -l | tr -d ' ')
echo "Uncommitted changes: $changes file(s)"
if git -C "$repo" remote get-url origin >/dev/null 2>&1; then
  echo "Remote: $(git -C "$repo" remote get-url origin)"
else
  echo "Remote: none (add one before pushing)"
fi
[[ -d "$repo/.github/workflows" ]] && echo "CI: workflows folder present" || echo "CI: none"
if [[ "$branch" == "main" || "$branch" == "master" ]]; then
  echo "STOP: on $branch - create a feature branch before changing anything."
  exit 1
fi
exit 0
