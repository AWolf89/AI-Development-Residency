---
name: ci-cd-setup
description: Sets up and maintains GitHub Actions CI for Python and JavaScript repos - running tests with an 80 percent coverage floor, lint and format checks (Ruff, ESLint, Prettier), and a dependency scan that fails on any vulnerability, on every push and pull request - with actions pinned to commit SHAs and least-privilege permissions, guided branch protection requiring CI to pass, and plain-language explanations of failures. Use when a repo has no .github/workflows folder, when git-workflow suggests it, when the user says CI, CD, GitHub Actions, pipeline, workflow file, build failing, checks failing, or deploy, or when a CI run fails on a PR. Deploy workflows are added only after the user picks a hosting provider and run only from a manual button. Do NOT use for local test planning (use test-planning), for commits and PRs themselves (use git-workflow), or for security reviews of app code (use security-review).
license: MIT
compatibility: Workflows run on GitHub Actions. Creating files works anywhere; reading CI logs needs the GitHub CLI (gh) or the user pasting logs. The user changes GitHub settings themselves.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.1.0
  category: devops
  tags:
  - ci
  - github-actions
  - pipeline
  - deployment
---

# CI/CD Setup

CI is a quality-control station on the factory line: every push is checked
automatically, so broken code is caught before it reaches `main`. CD is the conveyor
belt that ships what passed - here, only when the user presses the button.

## Critical rules

1. **Every `uses:` is pinned to a full commit SHA** with a version comment
   (`@3d3c... # v7.0.1`). Never a tag or branch alone.
2. **Least privilege:** every workflow sets top-level `permissions: contents: read`,
   and adds more only to the job that needs it, with a comment saying why.
3. **The dependency scan fails on any vulnerability, with no exceptions** - not even
   accepted risks. The fix is to upgrade or replace the package (see Troubleshooting).
4. **Deploys run only from a manual "Run workflow" button** (`workflow_dispatch`), and
   deploy workflows are added only after the user picks a hosting provider.
5. **CI failures are explained and a fix is proposed, then Claude asks** before
   changing code or pushing.
6. **Never print secrets in logs**; reference them only as `${{ secrets.NAME }}`.
   Secrets setup belongs to secrets-management.
7. **GitHub settings are changed by the user**; Claude guides.

## Step 1: Check the repo

Note the language(s) and whether `.github/workflows/` exists. Pick the template per
project: `assets/ci-python.yml` or `assets/ci-javascript.yml` (both, as two files, for a
repo with both). Explain the overall flow in plain language - not every line.

## Step 2: Prepare the project

The templates expect:
- Python: `requirements.txt` (and `requirements-dev.txt` if present), tests in `tests/`,
  Ruff config in `pyproject.toml` or `ruff.toml`.
- JavaScript: `package-lock.json`, and npm scripts `lint`, `format:check`, and
  `test:coverage` (the coverage tool's config must enforce an 80 percent floor).
Add missing config with sensible defaults (`references/tools.md`) and tell the user.

## Step 3: Add the workflow

Copy the template to `.github/workflows/ci.yml` (or `ci-python.yml` / `ci-javascript.yml`
for both). Then run:

```bash
python3 scripts/check_workflow.py .github/workflows/
```

It must pass (pins, permissions, triggers). Commit and push through git-workflow.

## Step 4: Watch the first run

```bash
gh run list --limit 3
gh run watch
```

If it fails, follow Step 6. When green, go to Step 5.

## Step 5: Require CI before merging (one-time)

Guide the user to add the CI job as a required status check on `main`
(`references/branch-protection-ci.md`). The check only appears in GitHub's list after
the workflow has run once.

## Step 6: When CI fails

1. Read the log: `gh run view <id> --log-failed` (or ask the user to paste it).
2. Explain in plain language which check failed and why.
3. Propose a fix and ask before changing code or pushing.
Patterns: `references/failure-triage.md`.

## Step 7: Deploys (later)

When the user picks a hosting provider, read `references/deploy-later.md` and add a
`workflow_dispatch` deploy workflow using the provider's official docs.

## Examples

**New Python repo.** git-workflow suggested CI.
Actions: copy ci-python.yml; add a Ruff config; run check_workflow (pass); commit and
push via git-workflow; watch the run; guide the user to require the check on main.

**Failing PR.** pip-audit reports a vulnerable `requests` version.
Actions: explain (a known flaw in a package you use - like a recalled part); propose
upgrading the pin; ask; on yes, update, push, watch.

**User asks to skip the scan "just this once".** Explain Rule 3 is their own rule; offer
the upgrade path; if they want the rule changed, that is a skill change (version bump),
not a one-off skip.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Scan fails, no fixed version exists | Package has an unpatched flaw | Replace the package or remove the feature using it; discuss with the user. Rule 3 has no exceptions |
| Coverage below 80 percent | Missing tests | Hand to test-planning; never lower the floor |
| `ruff format --check` / Prettier fails | Unformatted code | Run the formatter locally, commit |
| Required check not listed in GitHub | Workflow hasn't run yet | Push once, then add it |
| `npm ci` fails | Missing or stale package-lock.json | Run `npm install` locally and commit the lockfile |
| Action version outdated | Pins don't auto-update | See "Updating pins" in references/tools.md |

## Where this skill stops

It builds and maintains pipelines and explains failures. Tests are written by
test-planning; commits and PRs by git-workflow; secrets by secrets-management.
