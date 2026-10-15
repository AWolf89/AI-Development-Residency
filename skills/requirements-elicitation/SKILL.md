---
name: requirements-elicitation
version: 0.1.0
owner: AWolf89
description: Produces a numbered requirements document with acceptance criteria by interviewing the requester first about users, the underlying problem, scope boundaries, success measures, and edge cases. Use when the user asks to write requirements, a spec, a PRD, user stories, acceptance criteria, or a scoping document, and also when they describe a feature, integration, pipeline, or automation they want built but have not said who it is for, what is explicitly out of scope, or how success will be measured. Do NOT use for reviewing or critiquing requirements that are already written, for implementing or estimating work once requirements are agreed, or for project plans, roadmaps, and status documents.
---

# Requirements Elicitation

A one-line idea does not contain enough information to build from. The gap gets filled
somehow — and if nobody asks, it gets filled with assumptions that look confident in a
document and turn out wrong in production. The job of this skill is to move those
assumptions out of your head and the requester's head and onto the page, where they can
be challenged before anyone writes code.

So the order matters: **interview first, document second.** Producing a polished spec from
an unexamined one-liner is the exact failure this skill exists to prevent.

## Step 1: Calibrate depth

Match the interview to what is actually at stake. Over-interviewing a trivial ask is its own
failure — it wastes the requester's patience and trains them to route around you.

Judge the ask against these, and go to the deeper tier if signals are mixed:

| Tier | Signals | Interview |
|---|---|---|
| **Light** | One component, one known user group, reversible, no new data or integrations | 3–5 questions, single round |
| **Standard** | Multiple components or teams, new data flows, real users affected, moderate cost to get wrong | 6–10 questions, one round plus follow-ups |
| **Deep** | Cross-system, external parties, money, personal or regulated data, migration, hard to reverse | Full interview across all areas, expect 2+ rounds |

State the tier and why in one sentence before you start asking, so the requester can
redirect you: *"This touches payment data and two services, so I'll go deep — expect about
a dozen questions."*

## Step 2: Interview

Draw questions from `references/question-banks.md`. It holds a universal core plus banks for
software features, data and integrations, and automation and internal tooling. Open it before
asking — the per-domain questions are where the valuable edge cases hide, and they are not
worth re-deriving from memory each time.

For anything with users, data retention, performance expectations, or access control, also
open `references/nfr-catalog.md`. Non-functional requirements are the ones most often
remembered too late, when they are expensive.

How to run it well:

- **Ask in batches, not one at a time.** A single message with 5 numbered questions respects
  the requester's time far more than five round trips.
- **Lead with the problem, not the solution.** People arrive with a solution already chosen.
  Asking what breaks today, and for whom, often reveals that the proposed solution addresses
  a symptom.
- **Propose, don't interrogate, when you can infer.** "I'm assuming internal staff only, not
  customers — correct me if not" gets a faster, better answer than an open question, and it
  surfaces your assumption either way.
- **Chase vagueness immediately.** "Fast", "secure", "user-friendly", "handle errors
  gracefully", "scalable" are placeholders, not requirements. Convert each into something
  observable: fast becomes a latency number, secure becomes named threats and controls.
- **Follow the interesting thread.** A scripted interview that ignores a revealing answer is
  worse than no script. If they mention a workaround spreadsheet, ask about it.
- **Ask what happens when it fails.** Requesters describe the happy path by default. The
  error, empty, concurrent, and rollback cases are where requirements are actually missing.

If the requester cannot answer something, that is itself a finding: record it as an **open
question** with who needs to resolve it. Do not quietly fill the gap.

## Step 3: Confirm before documenting

Play back your understanding in a few lines — the problem, the users, the boundary — and ask
whether you have it right. Correcting a misunderstanding here costs a sentence; correcting it
after a full spec is written costs a rewrite and some of the requester's trust.

## Step 4: Produce the document

Write the output using `templates/requirements-doc.md`. The structure is fixed on purpose:
downstream skills and reviewers rely on the numbering and section names, so keep them exactly
as given.

The rules that make requirements usable — atomicity, testability, banned vague terms, how to
write acceptance criteria — are in `references/writing-rules.md`. Read it before writing the
first requirement rather than fixing violations afterward.

Non-negotiables for the document itself:

- Every requirement gets a stable ID (`FR-1`, `NFR-1`, `CON-1`) so later work can trace to it.
- Every functional requirement carries at least one acceptance criterion in Given/When/Then
  form. A requirement no one can test is a wish.
- Anything you assumed rather than heard goes in **Assumptions**, visibly, not buried in prose.
- Anything unresolved goes in **Open questions** with a named owner.
- **Out of scope** is never empty. If you cannot name what this excludes, the scope is not yet
  defined and you need another question.

## Step 5: Validate, then hand off

Run the bundled checker over the finished document:

```bash
python3 scripts/validate_requirements.py <path-to-document.md>
```

It mechanically checks ID numbering and uniqueness, missing acceptance criteria, vague
wording, compound requirements, and empty required sections. These are the failures worth
catching deterministically every time rather than re-deriving by eye. Fix what it reports, or
note why a flag is acceptable; do not hand over a document with unreviewed findings.

Close by telling the requester what to check first — usually the assumptions and open
questions, since those are where their knowledge beats yours.

## Where this skill stops

Produce the document and stop there. Do not begin implementing, estimating, or scheduling the
work in the same breath. The requester needs a chance to correct the spec while it is still
cheap, and bundling a build into the handoff removes that chance.
