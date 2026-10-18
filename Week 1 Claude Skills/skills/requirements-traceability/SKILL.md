---
name: requirements-traceability
description: Decomposes a spec, ticket, or multi-part request into numbered requirements before work starts, maps each piece of delivered output back to them during the work, and closes with a coverage report marking every requirement met, partially met, or not addressed with evidence and an explanation for anything incomplete. Use when the user hands over a spec, PRD, requirements document, acceptance criteria, RFP, ticket, or any request with several distinct asks and expects all of it covered, and whenever they ask whether everything was done, what was missed, or for a coverage or completeness check of delivered work. Do NOT use for eliciting or writing requirements that do not exist yet, for reviewing a spec's quality or ambiguity, or for project status reporting, estimation, and roadmaps.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.2.0
  category: product
  tags: [requirements, coverage, qa]
---

# Requirements Traceability

The failure this prevents is specific: work that addresses most of a request, reads as
complete, and never names the parts it skipped. Nobody decides to omit requirement 7 — it
falls off during the work, and the summary at the end describes what was built rather than
what was asked. The reader has no way to notice.

Traceability fixes that by making the requirement list, not the work, the thing you report
against. Three steps: decompose up front, map as you go, report honestly at the end.

If the requirements do not exist yet, this is the wrong skill — elicit them first, then
trace against the result.

## Step 1: Decompose before starting

Extract every distinct ask into a numbered list, and get it agreed before doing the work.
Decomposing afterward defeats the purpose: you will unconsciously derive the list from what
you happened to build.

Run the extractor over the source rather than eyeballing it:

```bash
python3 scripts/extract_requirements.py <spec-file> --out trace.json
```

It pulls existing IDs (`FR-1`, `NFR-2`, `AC-1.1`) when the source is already structured, and
otherwise splits prose into candidate requirements by obligation language and list structure.
Treat its output as a draft you correct, not an answer — it cannot tell a requirement from an
aside, and `references/decomposition.md` covers the judgment calls: compound sentences,
implied requirements, constraints that read as background, and how to handle acceptance
criteria that belong to a parent requirement.

Two rules that matter more than the rest:

- **Split anything that can be half-done.** If part of a line could be delivered while
  another part is skipped, they are two requirements. Compound items are exactly where silent
  omissions hide, because partial delivery still looks like a tick.
- **Capture what was implied but not stated.** A request to add a field usually implies
  display, validation, and persistence. Record these as derived requirements, marked as your
  inference, so the requester can strike them rather than discover them missing later.

Show the numbered list and ask for confirmation before starting. State the count: *"I read 11
requirements here, 3 of them inferred — confirm or correct before I start."*

## Step 2: Map while working, not afterward

Keep the trace current as you deliver each piece. Reconstructing it at the end is both
unreliable and biased toward the conclusion that everything was covered.

For each requirement record where it was satisfied — file and function, document section,
config change, test name — in the `evidence` field of `trace.json`. Evidence is what makes
the report checkable by someone who was not watching you work.

When you hit something that cannot be done as written — a conflict, a missing dependency, a
decision that is not yours — do not quietly route around it. Mark it blocked, note why, and
raise it. A requirement that silently becomes impossible is the costliest kind to discover
late.

If the requester changes direction mid-work, add or supersede requirements explicitly rather
than editing the list to match what you did. The history of what changed is part of what
makes the final report trustworthy.

## Step 3: Report coverage honestly

Produce the report using `templates/coverage-report.md`, then verify it:

```bash
python3 scripts/check_coverage.py trace.json
```

The checker enforces the properties a reader relies on: every requirement from the source
appears exactly once, no invented IDs, statuses drawn only from the allowed set, and every
status other than `met` carrying an explanation. It also computes the counts so the summary
line cannot drift from the table beneath it.

Statuses and what each one actually claims — `references/status-definitions.md` has the full
rules and the common misuses:

| Status | Claim being made |
|---|---|
| `met` | Delivered and verified against the acceptance criteria |
| `partial` | Some of it delivered; the gap is named |
| `not-met` | Not delivered; the reason is named |
| `blocked` | Cannot proceed; the blocker and who can clear it are named |
| `deferred` | Deliberately postponed with the requester's agreement |
| `superseded` | Replaced by a later requirement, which is referenced |

The one that gets abused is `met`. It claims verification, not intention — if you wrote the
code but never ran it, that is `partial` with the gap stated as unverified. Overclaiming here
destroys the value of the whole report, because a reader who finds one false `met` can no
longer trust any of them.

Lead the report with what is **not** fully covered. A reader scanning a wall of green ticks
will not find the one amber row halfway down, and the point of the exercise is to make
omissions impossible to miss.

## Examples

**Example — a multi-part ticket**
User hands over a ticket with 8 bullet points.
Actions:
1. `python3 scripts/extract_requirements.py <ticket> --out trace.json`; correct the draft list; mark inferred items.
2. Show "11 requirements, 3 inferred — confirm before I start."
3. Map evidence (file/function, test name) into `trace.json` as each piece is delivered.
4. `python3 scripts/check_coverage.py trace.json`; write the report from the template, leading with what's not fully covered.
Result: every bullet is accounted for, with evidence — including the two that turned out blocked.

## Troubleshooting

**`check_coverage.py` reports an invented ID.**
Cause: a requirement ID in the report doesn't exist in the source list.
Fix: remove it or trace it to the real source ID; the report must map 1:1 to the agreed list.

**Everything is marked `met`, but some of it was never run.**
Cause: `met` is being used for "written," not "verified."
Fix: downgrade unverified items to `partial` with the gap stated. One false `met` makes a reader distrust all of them.

**A requirement became impossible mid-work.**
Cause: a conflict or missing dependency surfaced after starting.
Fix: mark it `blocked` with the reason and who can clear it, and raise it — don't route around it silently.

## Composing with other skills

This skill tracks coverage; it does not write requirements, judge their quality, or do the
underlying work. When a request needs several of those, run them in sequence rather than
expanding this skill to cover them.
