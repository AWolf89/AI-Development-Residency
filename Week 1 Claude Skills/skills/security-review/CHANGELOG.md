# Changelog

Versions follow semantic versioning (MAJOR.MINOR.PATCH).

## [0.1.0] - 2026-10-19
### Added
- Initial skill: task and release reviews covering OWASP Top 10, APIs, Docker, n8n
  workflows, and dependencies; Critical/High/Medium/Low ratings; plain-language
  explanations with attacker view and analogy (no exploit code); auto-fix only Low,
  no-behaviour-change, this-task code; release gate on open Critical/High with recorded
  risk acceptance and review dates; dated reports in docs/security/.
- Dependency scanning (pip-audit, npm audit); Semgrep and Trivy planned.
- Scripts: dep_audit.sh, check_report.py. Report and accepted-risks templates. Evals.
