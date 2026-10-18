# Changelog

Semantic versioning: major for a changed Notion schema or page contract, minor for new
behavior, patch for fixes.

## [0.2.0] — 2026-10-17

### Changed
- Aligned with Anthropic's "Complete Guide to Building Skills": moved version and owner into a `metadata` block (author, owner, version, category, tags) and reviewed the instruction body against the guide's structure.

## [0.1.0] — 2026-10-15

Initial draft. Not yet released.

### Added
- Offer at the end of every substantial conversation (per the owner's decision), using a
  tappable Create summary / Skip choice, with plain-text fallback where that UI is absent.
- Three depth tiers that scale to how far the session went (per the owner's decision), with
  section templates in `references/summary-template.md`.
- `references/notion-schema.md` — database location, the three-property contract (Summary
  name / Summary date / Topics covered), one-time setup, tag rules, duplicate check, push
  sequence, and failure handling.
- `scripts/match_tags.py` — maps proposed topics onto existing multi-select tags (case,
  plurals, punctuation, short alias list) to prevent tag drift. Reports genuinely different
  synonyms as new rather than guessing.

### Design notes
- **The tap is the approval.** Per the owner's decision, Create summary pushes immediately
  and then shows the link. This satisfies the checklist's confirmation requirement for side
  effects: the tap is an explicit, per-summary user action, not an inferred one.
- **Creating the database is NOT covered by the tap.** A schema change is structural and
  one-time, so the skill stops and asks before creating it.
- **Idempotent by duplicate check.** Re-running on one session updates the existing row.
- **No Notion script.** The execution environment cannot reach Notion's API, and the
  connector carries the user's own permissions — the least-privilege route anyway.
- **Reliability depends on a user preference.** Triggering at the end of a conversation is
  state-based, the same weakness validation found in prompt-coaching. The description lists
  real phrasings, but the end-of-conversation offer is made reliable by a standing preference
  rather than by the description alone.

### Fixed during build
- Tag matcher treated "APIs" as new because the plural rule protecting "analysis" also
  blocked "apis"; now tries a plural-stripped fallback. Also added "-sses" plurals
  (classes, processes, addresses). Regression-tested on words that must survive intact.

### Known gaps before release
- Owner is `TBD`. Eval suite not run; description not variance-tested.
- The database does not exist yet; first use will trigger the setup question.
