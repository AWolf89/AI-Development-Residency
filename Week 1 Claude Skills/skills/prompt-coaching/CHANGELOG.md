# Changelog

Semantic versioning: major for a changed log-file contract, minor for new behavior, patch for fixes.

## [0.3.0] — 2026-10-17

### Added
- Troubleshooting section in `SKILL.md`.

### Changed
- Aligned with Anthropic's "Complete Guide to Building Skills": moved version and owner into a `metadata` block (author, owner, version, category, tags) and reviewed the instruction body against the guide's structure.

## [0.2.0] — 2026-10-15

### Changed
- **Description rewritten around observable user phrasings.** At 0.1.0 the description
  triggered on conversation state ("after completing a task"), which meant three of five
  trigger prompts had near-zero vocabulary overlap with it (mean 0.12) — a §1 never-triggers
  risk. It now leads with what users actually say: "that's not what I meant", "why did you
  build it that way", "was my request clear", "where was I vague", "how could I phrase this
  better", "we keep going back and forth". Measured overlap rose to 0.35.
- Exclusions extended to name writing-style critique, prompt-engineering training material,
  and requirements-document review, which are the nearest misses.
- Minor version bump rather than patch: this changes when the skill fires.

### Known limitation
- The trigger eval "write up what we did on the export project" still has zero overlap and
  always will — it is a task prompt with no coaching vocabulary in it. Coaching on that case
  depends on the skill being active for the task, not on the description matching the
  message. That eval should be reclassified as output-quality rather than triggering.

## [0.1.0] — 2026-10-14

Initial draft. Not yet released.

### Added
- Per the owner's decision, feedback is given after every substantial task — with explicit
  carve-outs for trivial exchanges, already-clear requests, and a stated preference against it.
- Fixed feedback shape: quoted phrase, the assumption made, and the specific rewording that
  would have removed the guess.
- `references/ambiguity-patterns.md` — ten categories with the guess each forces and the
  wording that closes it.
- `references/feedback-style.md` — phrasings that land versus grate, tone rules, failure
  modes, and when to say nothing.
- `scripts/log_ambiguity.py` — logs coaching points by category and reports which patterns
  actually recur, with a raised-already state so a pattern is surfaced once rather than
  repeatedly. Local JSON only; stores a short task label, not task content.

### Design notes
- Counting recurrence is mechanical because impression is biased toward recency; the loudest
  recent guess is usually not the real pattern.
- Hard boundary: blocking ambiguity gets a question during the work. Coaching covers
  reasonable assumptions, never questions that should have been asked.

### Known gaps before release
- Owner is `TBD`. Eval fixtures not written. Eval suite not run; description not variance-tested.
