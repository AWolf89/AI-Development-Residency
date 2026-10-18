# Changelog

Semantic versioning: major for a changed scope-file contract, minor for new behavior, patch for fixes.

## [0.2.0] — 2026-10-17

### Added
- Examples and Troubleshooting sections in `SKILL.md`.

### Changed
- Aligned with Anthropic's "Complete Guide to Building Skills": moved version and owner into a `metadata` block (author, owner, version, category, tags) and reviewed the instruction body against the guide's structure.

## [0.1.0] — 2026-10-14

Initial draft. Not yet released.

### Added
- Declare-boundary-first workflow: scope stated and written to `scope.json` before the first edit.
- Observation handling: noticed problems are reported, never acted on. Per the owner's
  decision, the default for an out-of-scope problem is note-and-don't-touch; only a problem
  that would make the delivered change unsafe is raised immediately.
- `references/boundary-cases.md` — the ambiguous cases: blocking vs non-blocking bugs,
  orphaned code, pre-existing test failures, formatter rewrites, poor surrounding style,
  missing helpers, outdated dependencies, config and CI files, documentation, and
  destructive operations.
- `templates/scope-declaration.json` — machine-checkable boundary with explicit out-of-scope
  list, dependency and config authorization flags, recorded widenings, and observations.
- `scripts/check_scope.py` — compares actual changes (git diff, or an explicit file list)
  against the declaration. Separates severity: changing an explicitly-excluded file and
  touching dependency/CI files without authorization are violations, while undeclared files
  not changed and reformat-shaped diffs are warnings.

### Design notes
- Severity is deliberately asymmetric. A skipped improvement costs a follow-up ticket; an
  unrequested change costs reviewer trust and possibly an incident.
- The declaration exists mainly so the user can widen the boundary *before* work starts
  rather than discover it in the diff.

### Known gaps before release
- Owner is `TBD`. Eval fixtures not written. Eval suite not run; description not variance-tested.
