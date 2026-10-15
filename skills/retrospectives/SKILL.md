---
name: retrospectives
version: 0.1.0
owner: AWolf89
description: Closes out a piece of work with a short retrospective covering what worked, what needed correcting and why, and what should change next time, then logs each correction so that one recurring a second time is proposed in writing as a new rule for a named skill, awaiting approval before any skill file is edited. Use after work that required real correction, rework, or a change of direction, when the user asks what we learned or what should change, and when deciding whether a repeated correction belongs in a skill. Do NOT use after work that went cleanly, for production incident postmortems, for coverage or completeness reporting on requirements, or for feedback on how the user phrased their request.
---

# Retrospectives and Lessons Learned

The same correction given three times is a missing rule, not three mistakes. Without somewhere
to accumulate, corrections evaporate at the end of each conversation and the user re-teaches
the same lesson indefinitely. This skill is the mechanism that turns a correction into a
durable change — and the reason the rest of the skill library improves rather than ossifies.

Two constraints shape everything below. **Rules are proposed in words and never applied
without approval**, because a skill edit changes behavior across every future task and that
authority belongs to the owner. And **a correction must generalize before it becomes a rule**,
because a library overfitted to specific incidents gets worse, not better — it accumulates
narrow prohibitions that misfire on the next task.

## When to run one

Run a retrospective after work that needed real correction: rework, a change of direction, a
misunderstanding that cost time, or repeated clarification. The trigger is correction, not
completion — work that went cleanly does not need one, and manufacturing lessons from a smooth
task produces noise that devalues the real ones.

What counts as a real correction, versus normal iteration that should not be logged, is in
`references/correction-taxonomy.md`. The distinction matters: treating ordinary refinement as
a correction inflates counts and promotes rules that should never exist.

Skip when: the work went cleanly, the user is mid-flow and the retro would interrupt, or they
have declined retros. Keep it to a few lines at the end of the work, not a separate ceremony.

## What goes in it

Use `templates/retrospective.md`. Four short sections, in this order.

**What worked** — specific, not courteous. "Declaring the file boundary up front meant the
diff matched the request" is useful; "good collaboration" is filler. Naming what worked
protects it from being changed away in a later revision.

**What needed correcting** — each correction with what happened, what the user had to say, and
the underlying cause. The cause is the part that matters: *"I assumed the test suite ran in
CI"* is a cause, *"the tests failed"* is a symptom, and only causes generate useful rules.

**Why** — the honest explanation. Missing context you could have asked for, an assumption that
seemed safe, an instruction you had but did not apply, or a genuine judgment call that went the
other way. Each points at a different fix, and only one of them is a skill change.

**What should change** — the concrete proposal, which may be none. Options are a new or
amended rule in a named skill, a change in how requirements are written, something to ask
earlier next time, or nothing at all because it was a one-off.

Be straightforward about your own errors without excessive self-criticism. The point is a
usable lesson, not contrition; a retro that reads as apology invites the user to reassure you
instead of engaging with the fix.

## Logging and the two-occurrence threshold

Log each correction so recurrence is counted rather than remembered:

```bash
python3 scripts/log_corrections.py --add --category <category> \
    --what "<what went wrong>" --cause "<underlying cause>" --skill <target-skill> --task "<label>"
python3 scripts/log_corrections.py --report
```

Counting belongs in a script because memory over-weights the most recent correction and
under-weights the one from three tasks ago. At **two occurrences** of the same cause, the
script surfaces it as a rule candidate.

A candidate is not yet a proposal. Before proposing, apply the generalization test in
`references/rule-writing.md`. The short form: a rule must be likely to fire correctly on
*future, different* tasks. Two occurrences of the same cause in the same unusual situation is
a coincidence with a sample size of two, and the right response is to keep logging, not to
write a rule. When a candidate fails the test, record that and let it keep accumulating.

## Proposing a rule

When a candidate passes, propose it in writing and stop there:

> **Proposed rule** for `scope-discipline`: when a change requires touching a file outside the
> declared boundary, stop and ask before editing, rather than widening the declaration and
> continuing.
> **Why:** this came up on the export task and again on the import fix — both times the diff
> grew past what you'd approved.
> **Where it would go:** the "Work inside it" rules in `SKILL.md`.
> **Risk:** it adds a pause on tasks where widening would have been uncontroversial.
>
> Want me to draft the edit?

Everything in that shape earns its place: the rule in the words it would be written in, the
evidence that it recurs, the file it belongs in, and the cost of adopting it. The risk line
matters most — a proposal with no stated downside has not been thought through, and every rule
costs something.

Then wait. Do not edit the skill, do not draft the change unasked, and do not re-propose a
declined rule. A declined proposal is information: log it and let it go.

## When not to make a rule

Not every correction should become one, and `references/rule-writing.md` covers this in full.
The common cases: it was a one-off with no general lesson; the real fix is in how requirements
are written rather than in a skill; an existing rule already covers it and was simply not
applied, which is a different problem; or the rule would be so narrow it only fires on the
original incident.

A library of twenty sharp rules outperforms one of two hundred, and every rule added is one
more thing that can misfire.
