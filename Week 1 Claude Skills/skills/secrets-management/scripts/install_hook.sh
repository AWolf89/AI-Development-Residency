#!/usr/bin/env bash
# Install a gitleaks pre-commit hook that scans staged changes and blocks secrets.
# Usage: bash install_hook.sh <repo-path>
# Idempotent: re-running when our hook is installed does nothing.
# Refuses to overwrite a different existing hook (exit 3) so nothing is lost.
# Exit codes: 0 = installed or already present, 2 = bad input, 3 = other hook exists.
set -euo pipefail

if [[ $# -ne 1 || "$1" == "-h" || "$1" == "--help" ]]; then
  sed -n '2,6p' "$0"; [[ $# -eq 1 ]] && exit 0 || exit 2
fi
repo="$1"
[[ -d "$repo/.git" ]] || { echo "ERROR: $repo is not a git repo" >&2; exit 2; }
hook="$repo/.git/hooks/pre-commit"
marker="# managed-by: secrets-management skill"

if [[ -f "$hook" ]]; then
  if grep -q "$marker" "$hook"; then echo "Hook already installed: $hook"; exit 0; fi
  echo "ERROR: a different pre-commit hook exists at $hook; not overwriting." >&2
  echo "Show it to the user and ask how to combine them." >&2
  exit 3
fi

command -v gitleaks >/dev/null 2>&1 || echo "WARNING: gitleaks not installed yet; the hook will block commits until it is. See https://github.com/gitleaks/gitleaks" >&2

mkdir -p "$repo/.git/hooks"
cat > "$hook" <<HOOK
#!/usr/bin/env bash
$marker
# Blocks commits whose staged changes contain secrets.
if ! command -v gitleaks >/dev/null 2>&1; then
  echo "gitleaks is not installed; commit blocked. Install: https://github.com/gitleaks/gitleaks" >&2
  exit 1
fi
# Newer gitleaks uses 'git --staged'; older versions use 'protect --staged'.
if gitleaks git --help >/dev/null 2>&1; then
  gitleaks git --staged --redact --verbose
else
  gitleaks protect --staged --redact --verbose
fi
HOOK
chmod +x "$hook"
echo "Installed gitleaks pre-commit hook: $hook"
