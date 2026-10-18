# Changelog

Semantic versioning: major for a changed log-file or proposal contract, minor for new
behavior, patch for fixes.

## [0.2.0] — 2026-10-17

### Added
- Examples and Troubleshooting sections in `SKILL.md`.

### Changed
- Aligned with Anthropic's "Complete Guide to Building Skills": moved version and owner into a `metadata` block (author, owner, version, category, tags) and reviewed the instruction body against the guide's structure.

## [0.1.0] — 2026-10-14

Initial draft. Not yet released.

### Added
- Retrospective triggered by correction rather than completion, per the owner's decision:
  work that went cleanly gets no retro.
- Four-section output (what worked / what needed correcting / why / what should change) via
  `templates/retrospective.md`, with "nothing should change" as a legitimate conclusion.
- `references/correction-taxonomy.md` — nine correction categories, an explicit not-a-
  correction list (refinement, changed mind, new requirements, acknowledged ambiguity,
  exploration, preference), cause-vs-symptom mapping, and severity bands.
- `references/rule-writing.md` — the four-part generalization test, where a rule belongs,
  how to write one, the four-element proposal format, and the five legitimate "no rule"
  outcomes.
- `scripts/log_corrections.py` — logs corrections, groups them by caller-supplied cause key,
  surfaces candidates at the threshold, and tracks the proposal lifecycle
  (none → proposed → approved/declined) so a declined rule is never re-surfaced.

### Design notes
- **Threshold of two, with a guard.** Per the owner's decision, two occurrences make a
  candidate. Because two is a small sample, the script separately reports occurrences that
  share a cause *and* a task as a likely coincidence rather than a pattern, and the
  generalization test stands between candidate and proposal. A count alone never produces
  a rule.
- **Proposal only, never application.** Rules are proposed in the words they would be
  written in, with the target file and the misfire risk, then the skill waits. A general
  acknowledgement is not approval.
- **The script does not judge semantic sameness.** An early version grouped causes by word
  overlap and failed on two phrasings of the same environment mistake. Grouping is now an
  explicit `--cause-key` supplied by the caller, and auto-derived keys are flagged in the
  report so under-grouping stays visible.
- Rejects symptom-shaped causes at input, since "tests failed" cannot generate a useful rule.

### Known gaps before release
- Owner is `TBD`. Eval fixtures and conversation setups not written.
- Eval suite not run; description not variance-tested.
- The two-occurrence threshold is the main thing to watch in evaluation: if proposals start
  arriving for things that are not really patterns, raise it to three rather than adding
  more guards.
