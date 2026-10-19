# Changelog

Versions follow semantic versioning (MAJOR.MINOR.PATCH).

## [0.1.0] - 2026-10-19
### Added
- Initial skill: four modes (project setup, everyday coding, audit, leak response);
  manager-neutral secret-manager standard covering local, Docker, n8n, CI, and deploys;
  gitleaks pre-commit hook on every repo; TruffleHog audits with verification on chosen
  repos; rotate-first leak response with confirmation before history rewrites.
- Scripts: check_repo_hygiene.py, install_hook.sh. Triggering and functional evals.
