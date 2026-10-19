# Changelog

Versions follow semantic versioning (MAJOR.MINOR.PATCH).

## [0.1.0] - 2026-10-19
### Added
- Initial skill: Python and JavaScript CI templates on every push and pull request;
  tests with 80 percent coverage floor; Ruff / ESLint / Prettier; dependency scan failing
  on any vulnerability with no exceptions; actions pinned to commit SHAs (checkout
  v7.0.1, setup-python v7.0.0, setup-node v7.0.0, taken 2026-10-19); least-privilege
  permissions; guided required status check on main; failure explanations with
  ask-before-fix; manual-button deploys deferred until a host is chosen.
- Script: check_workflow.py. Evals.
