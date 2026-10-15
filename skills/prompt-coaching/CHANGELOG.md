# Changelog

Semantic versioning: major for a changed log-file contract, minor for new behavior, patch for fixes.

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
