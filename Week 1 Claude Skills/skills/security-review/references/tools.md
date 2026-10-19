# Tools

Verify install steps in each project's current docs before first use.

## Now: dependency scanning
- pip-audit (Python): https://github.com/pypa/pip-audit - `pip install pip-audit`
- npm audit (JavaScript): built into npm - https://docs.npmjs.com/cli/commands/npm-audit

Analogy: checking every part you bought against a manufacturer recall list.

## Later (add when the user is ready)
- Semgrep - reads your code for risky patterns (SAST): https://semgrep.dev/docs
  Analogy: a building inspector reviewing blueprints.
- Trivy - scans Docker images and config: https://trivy.dev
  Analogy: inspecting the shipping container, not just the house.
When adding one: explain it, add it to dep_audit.sh or a new script, bump the skill's
version, and update the CHANGELOG.
