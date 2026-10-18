# Enterprise Skill Build Checklist

A reusable gate-check for building Claude skills that are fit for organization-wide deployment.
Work top to bottom; a skill is not "done" until every **Must** item is checked.

This checklist is a **superset of Anthropic's "Complete Guide to Building Skills for Claude"**:
it includes every hard rule and best practice from that guide, plus enterprise add-ons
(ownership, security, safety) marked **[Enterprise]**.

> How to use: copy this file into a skill's PR, tick the boxes, and treat unchecked **Must**
> items as merge blockers. Run `tools/audit_skills.py <skill-dir>` to check the mechanical ones.

---

## 0. Plan first (before writing anything)

- [ ] **Must** — 2–3 concrete use cases written down, each with **trigger → steps → result**.
- [ ] **Must** — Single, clearly stated responsibility (one skill, one job).
- [ ] **Must** — Scope boundaries written: what it does **and** what it explicitly does NOT do.
- [ ] **Must** — Success criteria defined:
  - *Quantitative:* triggers on ~90% of relevant queries; target tool-call / token budget; 0 failed tool/API calls per run.
  - *Qualitative:* user doesn't have to prompt for next steps; completes without correction; consistent across sessions.
- [ ] **Must [Enterprise]** — Named owner / team recorded in the skill's `metadata` or the repo.
- [ ] Should — Checked for overlap with existing skills; no duplicate or conflicting triggers (`tools/collisions.py`).

---

## 1. Structure & naming (hard rules)

- [ ] **Must** — `SKILL.md` exists, spelled **exactly** that way (case-sensitive; not `skill.md`/`SKILL.MD`).
- [ ] **Must** — Folder name is **kebab-case**: no spaces, no underscores, no capitals.
- [ ] **Must** — Folder name **matches** the `name` field in frontmatter.
- [ ] **Must** — **No `README.md` inside the skill folder** (all docs live in `SKILL.md` or `references/`). A repo-level README for humans is separate — see §10.
- [ ] Should — Conventional folders only, each optional:

```
skill-name/
├── SKILL.md          # REQUIRED — frontmatter + core instructions
├── scripts/          # optional — executable, deterministic helpers
├── references/       # optional — detailed docs loaded on demand
└── assets/           # optional — templates, fonts, icons used in output
```

> Note: Anthropic's standard folder for output templates/boilerplate is `assets/`. `templates/`
> also works, but prefer `assets/` for portability.

---

## 2. Frontmatter (the part Claude reads to decide loading)

- [ ] **Must** — Opens and closes with `---` delimiters; valid YAML.
- [ ] **Must** — `name`: kebab-case, matches folder, does **not** start with "claude" or "anthropic" (reserved).
- [ ] **Must** — `description`: present, **under 1024 characters**, states BOTH what it does AND when to use it.
- [ ] **Must** — **No XML angle brackets (`<` or `>`) anywhere in frontmatter** (security: frontmatter enters the system prompt).
- [ ] Should — `license` set if open source (e.g. `MIT`, `Apache-2.0`).
- [ ] Should — `metadata` block with `author`, `version` (semver), and useful keys (`category`, `tags`, `documentation`, `support`).
- [ ] Should — `compatibility` (1–500 chars) if the skill needs a specific product, package, or network access.
- [ ] Should — `allowed-tools` set when the skill should be restricted to specific tools (least privilege).

---

## 3. Triggering — the `description` field

> This is where most skills fail. Claude always sees the description; it decides activation from it alone.

- [ ] **Must** — Third person and specific (no "helps with…").
- [ ] **Must** — Structure: **[What it does] + [When to use it] + [key capabilities]**, with real user phrasings.
- [ ] **Must** — Names trigger phrases users would actually type, and file types if relevant.
- [ ] **Must** — Includes exclusions / negative triggers ("Do NOT use for X") to prevent over-triggering.
- [ ] Should — Debug check: ask Claude "When would you use the X skill?" — it should quote the description back correctly.

**Pattern:**
> `"<What it produces> from <inputs/file types>. Use when the user mentions <triggers>. Do NOT use for <exclusions>."`

---

## 4. Progressive disclosure & size

- [ ] **Must** — Three levels respected: frontmatter (always loaded) → `SKILL.md` body (loaded when relevant) → linked files (loaded only as needed).
- [ ] **Must** — `SKILL.md` body is the decision layer; deep detail lives in `references/*` and is **linked explicitly** ("For X, read `references/x.md`").
- [ ] **Must** — `SKILL.md` kept under **5,000 words**.
- [ ] Should — Body kept lean (a few hundred lines max); no detail inline that a reference could hold.

---

## 5. Instruction quality (the `SKILL.md` body)

- [ ] **Must** — Critical instructions are near the top; use `## Important` / `## Critical` headers for must-not-skip steps.
- [ ] **Must** — Steps are specific and actionable: exact commands + what success looks like (not "validate the data").
- [ ] **Must** — **Error handling / troubleshooting** included (common failure → cause → fix).
- [ ] Should — Has an **Examples** section (user says X → actions → result).
- [ ] Should — No ambiguous language; for critical validation, bundle a script instead of prose (see §6).
- [ ] Should — Bundled resources referenced clearly where they're needed.

---

## 6. Determinism — code over instructions

- [ ] **Must** — Anything with one correct method (parsing, validation, API calls) is a **bundled script**, not prose.
- [ ] **Must** — Instructions reserved for genuine judgment calls.
- [ ] Should — Scripts are independently runnable and testable outside the skill (`--help` works).
- [ ] Should — Scripts fail loudly with clear messages and explicit exit codes on bad input.

---

## 7. Governance & security [Enterprise]

- [ ] **Must** — Semantic `version` in `metadata`; `CHANGELOG.md` maintained.
- [ ] **Must** — Stored as code in a repo and goes through PR review.
- [ ] **Must** — Least privilege: only the tools the skill needs (enforce with `allowed-tools`).
- [ ] **Must** — Side-effecting actions (send, publish, write, delete, pay) require explicit confirmation.
- [ ] **Must** — No hardcoded secrets; credentials pulled from the environment.
- [ ] **Must** — Bundled code reviewed like any dependency (it executes).
- [ ] Should — Inputs validated in scripts before use; actions surfaced so they're auditable.

---

## 8. Testing & evals (three levels)

- [ ] **Must — Triggering tests:** fires on obvious tasks, fires on paraphrased requests, does **not** fire on unrelated topics (negative cases).
- [ ] **Must — Functional tests:** valid outputs generated, tool/API calls succeed, error handling works, edge cases covered.
- [ ] **Must** — Triggering accuracy and output quality tracked **separately**.
- [ ] Should — **Performance comparison** vs. no-skill baseline (tool calls + tokens + corrections needed).
- [ ] Should — Evals re-run after every edit and across model versions; watch for over/under-triggering signals and fix the description.

---

## 9. Design principles (scale & safety)

- [ ] **Must** — **Composable:** works alongside other skills; doesn't assume it's the only one loaded.
- [ ] **Must** — **Portable:** works across Claude.ai, Claude Code, and the API (note any exceptions in `compatibility`).
- [ ] **Must [Enterprise]** — Idempotent: re-running does not cause damage or duplication.
- [ ] **Must [Enterprise]** — Safe-by-default: destructive steps gated behind explicit confirmation.
- [ ] **Must [Enterprise]** — Consistent output contract: exact format/structure defined for downstream reliance.
- [ ] **Must [Enterprise]** — Graceful failure: defined behavior for malformed/missing inputs, not just the happy path.

---

## 10. Distribution & sharing

- [ ] Should — **Repo-level `README.md`** (for humans, outside the skill folder) with what it does, install steps, and example usage/screenshots.
- [ ] Should — Install path documented: download/zip the folder → Claude.ai Settings > Capabilities > Skills, or drop into the Claude Code skills directory.
- [ ] Should — Positioned by **outcome, not features** ("set up a workspace in seconds," not "a folder of YAML").
- [ ] Should — `version` bumped in `metadata` on every release; changelog updated.

---

## 11. Release gate (final sign-off)

- [ ] All **Must** items above checked (`tools/audit_skills.py` passes).
- [ ] Owner has reviewed and approved.
- [ ] Version bumped and `CHANGELOG.md` updated.
- [ ] Eval suite green (triggering + functional).
- [ ] Documentation / examples current.

---

### Quick reference: the failure modes to design against

| # | Failure mode | Primary defense |
|---|--------------|-----------------|
| 1 | Won't upload / won't load | §1 exact `SKILL.md`, kebab-case folder, valid frontmatter |
| 2 | Never triggers / triggers wrongly | §3 description with triggers + exclusions |
| 3 | Blows the context budget | §4 progressive disclosure + size limit |
| 4 | Unreliable, re-derived logic | §6 deterministic scripts |
| 5 | Instructions not followed | §5 critical-at-top, concrete commands, bundled validation |
| 6 | Unsafe / ungoverned at scale | §7 governance + §9 safety |
| 7 | Silent regressions | §8 evals (triggering + functional) |

*Tip: `tools/audit_skills.py` checks the mechanical Musts; `tools/collisions.py` flags trigger overlap; the `skill-creator` skill can scaffold and review drafts against this checklist.*
