---
name: security-review
description: Reviews an app for security vulnerabilities - OWASP Top 10, API security, Docker configuration, n8n workflows, and package dependencies - rating each finding Critical, High, Medium, or Low, explaining the risk and how an attacker could use it in plain language, auto-fixing only Low-severity issues in this task's code, and blocking releases on unresolved Critical or High findings. Use when self-review-checklist flags a change that touches authentication, user input, secrets, data storage, or permissions, before every release, or when the user says "security review", "is this secure", "check for vulnerabilities", "audit dependencies", or "pen test my code". Do NOT use for routine code quality checks (use self-review-checklist), for leaked secrets or credential setup (use secrets-management), or for writing exploit code or attacking systems the user does not own.
license: MIT
compatibility: Works in Claude Code, Claude.ai, and the API. Dependency scans need a terminal with pip-audit and/or npm; without one, the review is done by reading code and manifests.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.1.0
  category: security
  tags:
  - security
  - owasp
  - vulnerabilities
  - dependencies
  - release-gate
---

# Security Review

Self-review checks for unlocked doors in the code just written. This skill walks the
whole property looking for ways an attacker could get in. The user's apps are public,
so assume every input is hostile. The user is learning security, so every finding is
explained: the risk, how an attacker could use it, and an analogy.

## Critical rules

1. **Explain attacks conceptually, never as working exploit code.** Describe what an
   attacker could do and why it works; don't write payloads or attack scripts.
2. **Auto-fix only Low-severity findings that don't change behaviour, and only in this
   task's code.** Everything Medium and above, and anything in other code, is reported
   and asked about.
3. **Release gate:** a release is blocked while any Critical or High finding is open.
   It is unblocked only when each is fixed or the user explicitly accepts the risk, which
   is recorded with a reason and review date in `docs/security/accepted-risks.md`.
4. **Rate every finding** with `references/severity.md`; when unsure between two levels,
   pick the higher.
5. **Leaked secrets go to secrets-management** (rotate first); don't handle them here.

## Step 1: Pick the mode

| Trigger | Mode | Scope |
|---|---|---|
| Self-review flagged a security-touching change | Task review | The changed code and what it touches |
| Before a release | Release review | The whole app |
| User asks | Ask which scope if unclear | |

## Step 2: Dependency scan

```bash
bash scripts/dep_audit.sh <repo>
```

It runs pip-audit for Python (requirements files or pyproject) and npm audit for
JavaScript (package.json), and summarises findings. First use: explain what a dependency
scan is (checking bought parts against a recall list) and give install steps from
`references/tools.md`. Code-pattern scanning (Semgrep) and container scanning (Trivy)
are planned for later - see `references/tools.md`; until added, cover those areas by
reading.

## Step 3: Manual review

Walk each area in `references/review-areas.md` that applies: OWASP Top 10, APIs, Docker,
n8n workflows, dependencies. For each finding record: location, severity, risk, how an
attacker could use it, analogy, proposed fix.

## Step 4: Fix or ask

- Low + no behaviour change + this task's code -> fix it, re-run tests, mark **Fixed**.
- Everything else -> mark **Open**, describe the proposed fix, and ask.
- User declines a fix -> it becomes **Accepted** only after they explicitly say so; add
  it to `docs/security/accepted-risks.md` using `assets/accepted-risks-template.md`.

## Step 5: Report

Write `docs/security/YYYY-MM-DD-<task-or-release>.md` from `assets/report-template.md`
(keep its structure exactly), then:

```bash
python3 scripts/check_report.py docs/security/<report>.md            # task review
python3 scripts/check_report.py docs/security/<report>.md --release  # release review
```

With `--release`, exit code 1 means the release is blocked (open Critical/High or an
expired accepted risk). Show the report summary in chat.

## Step 6: Hand off

- Task review passed -> suggest the git-workflow skill.
- Release review passed -> say the release can continue.
- Don't start either without the user.

## Examples

**Task review.** Self-review flags a new signup endpoint.
Actions: run dep_audit (clean); review input validation, password storage, rate
limiting; find no rate limit (Medium: an attacker could create thousands of fake
accounts - like a shop with no limit on free samples); ask before adding it; write the
report; check passes; suggest git-workflow.

**Release review.** "Getting ready to release v1.0."
Actions: whole-app review; a High finding (admin route without an access check) -> ask;
user wants to ship anyway -> explain the risk again, record acceptance with reason and
review date only on their explicit yes; `--release` check passes; release continues.

**Low auto-fix.** A missing security header in the new route -> add it (no behaviour
change), mark Fixed, explain what the header protects against.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `pip-audit` or `npm` not found | Not installed | Install steps in references/tools.md |
| npm audit lists issues in dev-only packages | Build tools, not shipped code | Still report; usually Low unless they run on user input |
| Unsure of severity | Borderline | Pick the higher level (Rule 4) |
| check_report fails --release | Open Critical/High or expired risk | Fix, or get explicit acceptance; renew expired risks with the user |
| Finding is a leaked secret | Wrong skill | Hand to secrets-management |
| No terminal | Surface limitation | Review manifests by reading; note "manual" in the report |

## Where this skill stops

It finds, rates, explains, and fixes Low issues. Code quality belongs to
self-review-checklist; secrets to secrets-management; commits to git-workflow.
