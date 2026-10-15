# Changelog

Semantic versioning: major for changed checkpoint behavior contracts, minor for new behavior, patch for fixes.

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
