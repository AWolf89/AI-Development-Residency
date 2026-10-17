# Changelog

All notable changes to the `requirements-traceability` skill. Semantic versioning: major for
a changed output or trace-file contract, minor for new behavior, patch for fixes.

## [0.1.0] — 2026-10-14

Initial draft. Not yet released — see open gate items below.

### Added
- Three-phase workflow: decompose and confirm before work, map evidence during work, report
  coverage at the end.
- `references/decomposition.md` — what counts as a requirement, splitting compound items,
  implied and derived requirements, acceptance criteria handling, extracting from unstructured
  tickets and threads, and granularity guidance.
- `references/status-definitions.md` — the six statuses, what each one claims, and the
  misuses of `met` in particular.
- `templates/coverage-report.md` — fixed report contract that leads with what is not covered.
- `scripts/extract_requirements.py` — structured mode preserves source IDs and attaches
  acceptance criteria to parent requirements; prose mode splits tickets and notes into
  candidates, skips background and out-of-scope sections, and flags compound items.
- `scripts/check_coverage.py` — validates statuses, requires evidence for `met` and an
  explanation for everything else, rejects filler and work-in-progress statuses, enforces
  ID uniqueness, and detects requirements dropped from or invented against the source spec.

### Design notes
- `met` requires checkable evidence by construction, because the report's whole value rests
  on that claim being reliable.
- The extractor over-splits deliberately: a spurious row costs a line of review, a missed
  one is the failure the skill exists to prevent.
- Composes with `requirements-elicitation` rather than absorbing it; structured mode reads
  that skill's output template directly.

### Known gaps before release
- Owner field in `SKILL.md` frontmatter is `TBD`.
- Eval fixtures (`invoice-export-spec.md`, `requirements-thread.md`) not yet written.
- Eval suite not yet run; description not yet variance-tested.
