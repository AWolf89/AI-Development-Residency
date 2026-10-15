# Coverage report: <work item>

**Source:** <spec, ticket, or thread the requirements came from> · **Date:** <YYYY-MM-DD>

## Summary

<N> requirements tracked · **<N> met** · <N> partial · <N> not met · <N> blocked · <N> deferred

<One sentence naming the overall state in plain terms — e.g. "Core import flow is complete
and verified; XLSX support and the audit log are not done.">

## Needs attention

Everything not fully covered, listed first so it cannot be missed. Remove this section only
when every requirement is `met`.

| ID | Requirement | Status | What is missing and why |
|---|---|---|---|
| R-7 | <requirement text> | partial | <specific gap, not a restatement of what was done> |
| R-9 | <requirement text> | blocked | <blocker, and who can clear it> |

## Full coverage

| ID | Requirement | Status | Evidence |
|---|---|---|---|
| R-1 | <requirement text> | met | <file/function, test name, or document section> |
| R-2 | <requirement text> | met | <evidence> |

## Derived requirements

Requirements inferred rather than stated in the source. Strike any that were not wanted.

| ID | Requirement | Inferred from | Status | Evidence |
|---|---|---|---|---|
| R-12 | <requirement text> | <the stated requirement it follows from> | met | <evidence> |

## Changes during the work

Requirements added, superseded, or re-scoped after the list was agreed.

| ID | Change | When and who agreed |
|---|---|---|
| R-4 | Superseded by R-14 | <date, requester> |

## Out of scope

Echoed from the source so that predictable "why wasn't X done" questions are answered up front.

- <item>

## Open questions carried forward

| # | Question | Owner |
|---|---|---|
| Q-1 | <unresolved item blocking or qualifying a requirement> | <name> |

---

### Notes on using this template

- Keep the ID prefix used in the source document. Do not renumber.
- Every row with a status other than `met` needs an explanation in its own cell.
- Delete empty sections only if they are genuinely empty — an absent "Needs attention"
  section is a strong claim, so make sure it is true.
- The summary counts must match the tables. `check_coverage.py` computes them for you.
