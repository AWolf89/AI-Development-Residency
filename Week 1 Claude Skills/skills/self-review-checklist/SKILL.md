---
name: self-review-checklist
description: Reviews Claude's own code against a fixed checklist before every code hand-off - correctness, security basics, error handling, logging, readability, docs, scope, and dependencies - auto-fixing small issues in its own new code, asking before big ones, and reporting results as a table of item, status, and evidence with plain-language explanations of each failure. Use before handing over any code Claude wrote or changed, of any size, including after test-planning finishes, when the user says "review your work", "self-review", "check this before I merge", or "is this ready". Do NOT use for reviewing code Claude did not write (such as a teammate's PR), for deep security audits (use security-review), or for answers that contain no code.
license: MIT
compatibility: Works in Claude Code, Claude.ai, and the API. The quick scan needs code execution; without it, checks are done by reading.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.1.0
  category: engineering
  tags:
  - code-review
  - quality
  - checklist
  - error-handling
  - logging
---

# Self-Review Checklist

Like a pilot's pre-flight checklist: the same items every time, so nothing gets skipped
when a task feels finished. Runs before every code hand-off.

## Critical rules

1. **Run before every code hand-off**, whatever the size. Code is not handed over until
   the review table is shown.
2. **Auto-fix only Claude's own new or changed code, and only small issues.** Small means
   no behaviour change (naming, comments, a missing error message, lint). Anything that
   changes behaviour, security, or design is big: describe it and ask before changing it.
3. **Never touch code outside this task.** Problems found there go under
   "Observations" for the user to decide on.
4. **Security basics and Scope are never N/A.** Other items may be N/A only with a reason.
5. **Never mark PASS without evidence** (a test name, file and line, or command output).

## Step 1: Pick the checklist

- **Tiny task:** short checklist - Correctness, Security basics, Scope.
- **Medium or new app:** full checklist - all 8 areas.

The items for each area are in `references/checklist.md`; read it every time rather than
working from memory. Error handling and logging rules are in `references/standards.md`.

## Step 2: Run the quick scan (when code execution is available)

```bash
python3 scripts/quick_scan.py <changed files or folders>
```

It flags mechanical problems: `print`/`console.log` instead of logging, empty or
catch-all exception handlers, and strings that look like hardcoded secrets. Each hit is
a lead to check, not an automatic fail - confirm by reading the code.

## Step 3: Check every item, fix or ask

For each item: check it, record evidence, then:
- passes -> **PASS**
- small issue in Claude's new code -> fix it -> **FIXED** (say what changed)
- big issue -> **FAIL** (do not fix; describe it and the proposed fix, ask the user)
- doesn't apply -> **N/A** with a reason (never for Security basics or Scope)

After any FIXED, re-run tests so the fix didn't break anything.

## Step 4: Report

Use this exact format (downstream skills rely on it):

```markdown
## Self-review: <task name>
Checklist: Short | Full

| Item | Status | Evidence |
|---|---|---|
| Correctness | PASS | 14 tests pass (pytest output) |
| Logging | FIXED | Replaced print() with logger.info in app/routes.py:42 |
| Security basics | FAIL | User input reaches SQL query unescaped (db.py:18) |
| Docs | N/A | No user-facing change |

### Failures explained
<For each FAIL and FIXED: what it means in plain language, why it matters, an analogy
if the concept is new, and for FAIL the proposed fix and the question for the user.>

### Observations (outside this task - not changed)
<Problems noticed in other code, or "None".>
```

Then validate the report:

```bash
python3 scripts/check_review.py <report.md>
```

## Step 5: Hand off

- Any FAIL left -> wait for the user's decision; do not hand off as done.
- All PASS / FIXED / N/A -> suggest the **security-review** skill if the change touched
  authentication, user input, secrets, data storage, or permissions; then suggest
  **git-workflow**. Do not start either without the user.

## Examples

**Medium feature.** After test-planning finishes an export endpoint.
Actions: full checklist; scan finds a `print()`; replace it with logging (FIXED); input
validation present (PASS); README missing the new endpoint - add it (FIXED); show the
table; endpoint reads user input, so suggest security-review, then git-workflow.

**Tiny change.** A renamed config variable.
Actions: short checklist; tests pass (PASS); no secrets or input touched (PASS, evidence:
diff); only the rename changed (PASS); suggest git-workflow.

**Big issue.** The new code builds an SQL query from user input.
Actions: mark Security basics FAIL, explain SQL injection with an analogy, propose a
parameterised query, ask before changing.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Unsure if an issue is small or big | Borderline behaviour change | Treat it as big and ask |
| Scan flags a test fixture as a secret | Fake value that looks real | Confirm it's fake, PASS with that evidence |
| Problem in old code | Outside this task | List under Observations; don't fix |
| Tests fail after a FIXED | The "small" fix changed behaviour | Revert it and reclassify as big |
| `check_review.py` fails | Missing item, bad status, or N/A without reason | Fix the report as it says |
| No code execution | Surface limitation | Check by reading; note "manual" in evidence |

## Where this skill stops

It reviews and makes small fixes to Claude's own new code. Deep security audits belong to
security-review; commits and PRs to git-workflow.
