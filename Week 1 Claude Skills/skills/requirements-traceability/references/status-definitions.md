# Status definitions

A coverage report is only worth reading if its statuses mean the same thing every time. The
risk is asymmetric: an overstated `met` destroys trust in every other row, while an
understated one costs a sentence of explanation. When genuinely torn, choose the weaker
claim and explain.

---

## met

**Claims:** delivered *and* verified against the acceptance criteria or the plain reading of
the requirement.

Requires evidence a reader can check: a file and function, a test name and its result, a
document section, a configuration change, a screenshot.

Not `met` when:
- The code is written but never executed or tested → `partial`, gap stated as unverified.
- It works in one case but the requirement covers several → `partial`.
- You believe it is handled by existing behavior but did not confirm → `partial`.
- It is done but the acceptance criteria were never checked → `partial`.

"I implemented it" and "it works" are different claims. Only the second is `met`.

## partial

**Claims:** part of this is delivered, and the remaining gap is named specifically.

An explanation is mandatory and must say what is missing, not restate what was done. "Export
works for CSV; XLSX not implemented" is usable. "Mostly complete" is not — the reader cannot
act on it.

Use `partial` for the honest middle ground: implemented but unverified, works for the main
case but not the edge cases, done for one environment but not the others.

## not-met

**Claims:** not delivered at all, with the reason stated.

Reasons worth distinguishing, because they lead to different next steps:
- Out of time or scope for this round.
- Depends on something that does not exist yet.
- Requires a decision or access you do not have.
- You judged it unnecessary — say so explicitly, since that is the requester's call to
  overturn, not yours to make silently.

`not-met` is not a failure state. An honest `not-met` with a clear reason is more valuable
than a generous `partial`.

## blocked

**Claims:** cannot proceed until something outside your control changes.

Must name the blocker and who can clear it. If you can work around it, it is not blocked.

Distinguish from `not-met`: blocked means the work stopped against an obstacle, not that it
was skipped or deprioritized. Blocked items belong at the top of the report because they need
someone else to act.

## deferred

**Claims:** deliberately postponed, with the requester's agreement.

The agreement is what separates `deferred` from `not-met`. If nobody agreed, it is `not-met`
however reasonable the postponement was — you do not get to defer unilaterally and record it
as a mutual decision. Reference when and where it was agreed.

## superseded

**Claims:** replaced by a later requirement, which must be referenced by ID.

Keeps the original visible rather than quietly deleting it, so a reader comparing the report
against the original spec does not find a missing number. Never renumber to close the gap.

---

## Rules that apply across all statuses

- **Every status except `met` carries an explanation.** The checker enforces this, because an
  unexplained gap is nearly as unhelpful as a hidden one.
- **One status per requirement.** If different parts have different outcomes, the requirement
  was under-decomposed; split it and status each piece.
- **Never change a status to match the summary.** Fix the summary.
- **Uncertainty is reportable.** "I could not determine whether this is satisfied by the
  existing auth middleware" is a legitimate note on a `partial`, and more useful than a
  confident guess in either direction.
