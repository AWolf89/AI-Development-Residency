---
name: scope-discipline
description: Keeps delivered work to exactly what was asked by declaring the file and change boundary before starting, refusing unrequested refactoring, renaming, dependency changes, reformatting, and extra features, and reporting anything noticed outside that boundary as an observation instead of acting on it. Use when implementing against a spec, ticket, or change request, when touching shared or production code, when the user says to change only a specific thing or not to touch anything else, and when a previous attempt did more than was wanted. Do NOT use when the user explicitly asks for a refactor, cleanup, or open-ended improvement, when exploring or prototyping where wandering is the point, or for deciding what the requirements should be.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.2.0
  category: engineering
  tags: [scope, code-review]
---

# Scope Discipline

Scope creep in AI-assisted work rarely looks like disobedience. It looks like helpfulness:
tidying a function while passing through, renaming a confusing variable, adding the error
handling that was obviously missing, upgrading a dependency that was out of date. Each
change is defensible alone. Together they produce a diff the reviewer did not ask for and
cannot safely approve, and the one line that actually mattered is buried inside it.

The cost is asymmetric and that is the whole justification for this skill. An improvement
you skipped costs a follow-up ticket. An unrequested change that breaks something costs an
incident, and it breaks the reviewer's ability to trust that the diff matches the request.

So: **do exactly what was asked, and write down everything else you noticed.** Noticing is
valuable. Acting on it unilaterally is not.

## Step 1: Declare the boundary before starting

Before the first edit, state what you intend to touch and what you will not:

> Scope: `src/export/csv.py` and its test file. I won't touch the shared `export/base.py`,
> won't change dependencies, and won't reformat anything I'm not already editing.

Write it to `scope.json` (see `templates/scope-declaration.json`) so it can be checked
mechanically rather than remembered. Declaring the boundary out loud is most of the work —
it converts a vague intention into something you and the user can both hold you to, and it
gives them a chance to widen it before you start rather than argue about it afterward.

If the boundary is genuinely unclear, ask. One question costs less than an unwanted diff.

## Step 2: Work inside it

The behaviors that constitute creep, and what to do instead, are in
`references/boundary-cases.md`. It covers the ambiguous ones — the bug you have to fix to
make your change work, the dead code your change orphans, the test that was already failing,
the formatter that rewrites the whole file on save.

The rules that cover most situations:

- **Touch the minimum that satisfies the requirement.** If a two-line change works, a
  twelve-line better-structured change is still the wrong answer.
- **Match surrounding conventions, even ones you dislike.** Consistency with the file beats
  your preference. Introducing a better pattern in one function makes the file worse.
- **No drive-by renaming, reordering, reformatting, or comment cleanup.** These produce diff
  noise that hides the real change from review.
- **No new dependencies, version bumps, config changes, or tooling changes** unless the
  request required them. Say so if one is genuinely needed and wait.
- **No unrequested features**, including ones the requirement implies would be nice. If you
  believe something is missing, that belongs in observations, where it is the requester's
  call.
- **Deleting is a change too.** Dead code, unused imports, and stale comments stay unless
  removing them was asked for.

When your change genuinely cannot work without touching something outside the boundary, stop
and say so with the specifics, rather than quietly widening it. A widened boundary the user
agreed to is fine; a widened boundary they discover in the diff is not.

## Step 3: Record observations instead of acting

Everything you notice but do not touch goes in an observations list: the bug two functions
over, the missing index, the test that asserts nothing, the duplicated logic.

For each, record what and where, why it matters, and roughly what fixing it would involve.
Keep them short — an observation is a pointer, not a proposal. This is the part people
actually value, because you noticed things while you were in there and they would rather know
than not. What they do not want is for you to have acted on it.

A noticed problem that would make your delivered change unsafe or wrong is different: raise
that immediately rather than filing it quietly at the end.

## Step 4: Verify the diff before handing over

Check what you actually touched against what you declared:

```bash
python3 scripts/check_scope.py scope.json          # uses git diff by default
python3 scripts/check_scope.py scope.json --files <list>   # when git isn't available
```

It flags files changed outside the declared boundary, dependency and config files touched
without declaration, and diffs whose shape suggests reformatting rather than targeted edits.
Memory is a poor instrument here — it is easy to forget a file you opened early and changed
casually — so run the check rather than recalling.

Then summarize for the reviewer: what changed, and the observations list. Lead with the
scope statement so they can verify the diff matches it at a glance.

## When the user widens scope

If they say "while you're in there, also…", that is a new boundary, not permission to
freelance. Update the declaration, state the new boundary, and keep working the same way.

## Examples

**Example — a focused bug fix**
User: "Fix the off-by-one in `csv.py`, don't touch anything else."
Actions: declare the boundary to `scope.json`; make the minimal change; note the unrelated missing-index issue as an observation instead of fixing it; run `check_scope.py scope.json`; hand over leading with the scope statement.
Result: a one-line diff the reviewer can approve at a glance, plus a pointer to what else you saw.

## Troubleshooting

**`check_scope.py` flags a file you changed casually.**
Cause: a file opened early and edited out of habit, outside the declaration.
Fix: revert it, or declare it explicitly and confirm with the user — don't let the diff grow past what was approved.

**Your change genuinely needs a file outside the boundary.**
Cause: a real dependency the declaration didn't anticipate.
Fix: stop and say so with specifics; widen the boundary with the user's agreement before continuing, never silently.

**The formatter rewrote the whole file on save.**
Cause: editor auto-format touched lines you didn't mean to change.
Fix: restore the unrelated lines so the diff shows only your targeted edit; see `references/boundary-cases.md`.
