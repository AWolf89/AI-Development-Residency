# Enterprise Skill Build Checklist

A reusable gate-check for building Claude skills that are fit for organization-wide deployment.
Work top to bottom; a skill is not "done" until every **Must** item is checked.

> How to use: copy this file into a skill's PR, tick the boxes, and treat unchecked **Must** items as merge blockers.

---

## 0. Scope & Ownership (before writing anything)

- [ ] **Must** — Skill has a single, clearly stated responsibility (one skill, one job).
- [ ] **Must** — Named owner / team is recorded in the skill or its repo.
- [ ] **Must** — Scope boundaries written down: what it does **and** what it explicitly does NOT do.
- [ ] Should — Checked for overlap with existing skills; no duplicate or conflicting triggers.

---

## 1. Triggering — the `description` field

> This is where most enterprise skills fail. Claude always sees the description; it decides activation from this alone.

- [ ] **Must** — Description is in the third person and specific (no "helps with…").
- [ ] **Must** — States **when** to use it: trigger words, file types, and real user phrasings.
- [ ] **Must** — Includes exclusions ("Do NOT use for X") to prevent collisions.
- [ ] Should — Keyword-rich with the vocabulary your users actually type.
- [ ] Should — Tested against near-miss prompts that should **not** trigger it.

**Pattern:**
> `"<What it produces> from <inputs/file types>. Use when the user mentions <triggers>. Do NOT use for <exclusions>."`

---

## 2. Progressive Disclosure — structure & context budget

- [ ] **Must** — `SKILL.md` body is the decision layer only (workflow, branching, which file to open next).
- [ ] **Must** — Deep detail (schemas, edge cases, long examples) lives in `references/*.md`, loaded on demand.
- [ ] **Must** — References are linked explicitly from the body ("For X, read `references/x.md`").
- [ ] Should — SKILL.md body kept lean (aim: a few hundred lines max).
- [ ] Should — Folder layout is conventional:

```
skill-name/
├── SKILL.md          # frontmatter + core instructions
├── references/       # on-demand detail
├── scripts/          # deterministic helpers
└── templates/        # output formats / boilerplate
```

---

## 3. Determinism — code over instructions

- [ ] **Must** — Anything with one correct method (parsing, validation, API calls) is a **bundled script**, not prose.
- [ ] **Must** — Instructions reserved for genuine judgment calls.
- [ ] Should — Scripts are independently runnable and testable outside the skill.
- [ ] Should — Scripts fail loudly with clear error messages on bad input.

---

## 4. Governance (the enterprise layer)

- [ ] **Must** — Semantic version recorded in frontmatter; changelog maintained.
- [ ] **Must** — Skill is stored as code in a repo and goes through PR review.
- [ ] **Must** — Least privilege: only the tools/permissions the skill actually needs are bundled.
- [ ] **Must** — Side-effecting actions (send, publish, write, delete, pay) require explicit confirmation.
- [ ] **Must** — No hardcoded secrets; credentials pulled from the environment.
- [ ] **Must** — Bundled code reviewed like any dependency (it executes).
- [ ] Should — Inputs validated in scripts before use.
- [ ] Should — Skill surfaces what it did, so actions are auditable/traceable.

---

## 5. Evals — test, don't vibe

- [ ] **Must** — Eval suite exists: realistic prompts covering happy path + edge cases.
- [ ] **Must** — Negative cases included (prompts that should NOT trigger the skill).
- [ ] **Must** — Triggering accuracy and output quality tracked separately.
- [ ] Should — Evals re-run after every edit and across model versions.
- [ ] Should — Variance/benchmark analysis run on the description before shipping.

---

## 6. Design Principles (scale & safety)

- [ ] **Must** — Idempotent: re-running does not cause damage or duplication.
- [ ] **Must** — Safe-by-default: destructive steps gated behind explicit confirmation.
- [ ] **Must** — Consistent output contract: exact format/structure defined for downstream reliance.
- [ ] **Must** — Graceful failure: defined behavior for malformed/missing inputs, not just the happy path.
- [ ] Should — Composable: prefers coordinating with other skills over becoming a monolith.

---

## 7. Release Gate (final sign-off)

- [ ] All **Must** items above checked.
- [ ] Owner has reviewed and approved.
- [ ] Version bumped and changelog updated.
- [ ] Eval suite green.
- [ ] Documentation/examples current.

---

### Quick reference: the five failure modes to design against

| # | Failure mode | Primary defense |
|---|--------------|-----------------|
| 1 | Never triggers / triggers wrongly | §1 Description with triggers + exclusions |
| 2 | Blows the context budget | §2 Progressive disclosure |
| 3 | Unreliable, re-derived logic | §3 Deterministic scripts |
| 4 | Unsafe / ungoverned at scale | §4 Governance + §6 safety |
| 5 | Silent regressions | §5 Evals |

*Tip: the `skill-creator` skill can scaffold a new skill, draft the description, and run eval/variance analysis against this checklist.*
