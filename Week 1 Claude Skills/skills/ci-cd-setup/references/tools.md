# Tools and defaults

Verify flags in current docs before first use.

| Tool | Job | Docs |
|---|---|---|
| Ruff | Python lint + format | https://docs.astral.sh/ruff |
| ESLint | JavaScript lint | https://eslint.org/docs |
| Prettier | JavaScript format | https://prettier.io/docs |
| pytest-cov | Python coverage | https://pytest-cov.readthedocs.io |
| pip-audit | Python dependency scan | https://github.com/pypa/pip-audit |
| npm audit | JavaScript dependency scan | https://docs.npmjs.com/cli/commands/npm-audit |

Default package.json scripts (adjust the test command to the project's framework):
```json
"lint": "eslint .",
"format:check": "prettier --check .",
"test:coverage": "vitest run --coverage"
```
Set the 80 percent floor in the test tool's coverage config.

## Updating pins
Pinned SHAs don't update themselves. Every few months, or when a security advisory
affects an action:
1. Find the new release tag on the action's GitHub releases page.
2. Prefer releases at least two weeks old (new releases can carry malicious code before
   anyone notices).
3. Get its commit SHA: `git ls-remote --tags https://github.com/<owner>/<action>.git`
   (for annotated tags, use the line ending in ^{}).
4. Update the SHA and the version comment, run check_workflow.py, and go through a PR.
Optional later: GitHub's Dependabot can propose these updates automatically.

Pins in the templates were taken on 2026-10-19: actions/checkout v7.0.1,
actions/setup-python v7.0.0, actions/setup-node v7.0.0.
