# Changelog

Semantic versioning: major for changed checkpoint behavior contracts, minor for new behavior, patch for fixes.

## [0.3.0] — 2026-10-17

### Changed
- Aligned with Anthropic's "Complete Guide to Building Skills": moved version and owner into a `metadata` block (author, owner, version, category, tags) and reviewed the instruction body against the guide's structure.

## [0.2.0] — 2026-10-15

### Changed
- **Description rewritten around observable user phrasings.** Validation showed the 0.1.0
  description shared almost no vocabulary with the prompts meant to trigger it (mean overlap
  0.14): it described a conversation state ("when they will own the result") rather than
  anything a user types. The rewrite leads with real phrasings — "new to", "not my area",
  "never dealt with this", "not sure what it does", "want to understand", "walk me through",
  "I'll be maintaining it" — and measured overlap rose to 0.25 with no near-zero positives.
- Exclusions extended to name tutorial, interview-prep, and incident cases explicitly, since
  those were the closest near-misses.
- Minor version bump rather than patch: this changes when the skill fires, which is behavior.

## [0.1.0] — 2026-10-14

Initial draft. Not yet released.

### Added
- Three-condition trigger test: the concept is load-bearing, no familiarity has been shown,
  and the user will own the result. Per the owner's decision, need is inferred from the
  conversation rather than waiting to be told.
- `references/signals.md` — strength-weighted signals of a gap and of fluency, the hard case
  of confident vocabulary over a shaky model, and guidance to read signals per concept
  rather than per person.
- `references/checkpoint-forms.md` — four forms from one-line flag to decision checkpoint,
  phrasings that undermine the practice, non-quizzing ways to confirm understanding, and the
  handover list.
- Session cap of one to two checkpoints, with over-checkpointing treated as a first-class
  failure mode.

### Design notes
- No bundled script. Nothing here has a single correct method; this is judgment work, and a
  script would be ceremony rather than reliability. The enterprise checklist asks for
  determinism where one correct method exists, not everywhere.
- The offer form ("want the short version?") is the default under uncertainty because it
  makes declining costless, so the answer is informative rather than face-saving.

### Known gaps before release
- Owner is `TBD`. Eval suite not run; description not variance-tested.
- Judgment-heavy outputs: qualitative review should carry more weight than assertions here.
