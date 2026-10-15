# Changelog

All notable changes to the `requirements-elicitation` skill. Versions follow semantic
versioning: major for a changed output contract, minor for new behavior, patch for fixes.

## [0.1.0] — 2026-10-14

Initial draft. Not yet released — see the open gate items in `evals/README.md`.

### Added
- Interview-first workflow with three depth tiers (light / standard / deep).
- `references/question-banks.md` — universal core plus banks for software features, data and
  integrations, and automation and internal tooling, with probes for vague answers.
- `references/nfr-catalog.md` — non-functional requirement categories and what a usable
  answer looks like for each.
- `references/writing-rules.md` — atomicity, testability, EARS sentence forms, banned vague
  terms, acceptance-criteria form, traceability.
- `templates/requirements-doc.md` — fixed output contract with stable ID prefixes
  (FR / NFR / CON / A / G / Q).
- `scripts/validate_requirements.py` — deterministic checks for ID uniqueness and sequence,
  missing acceptance criteria, Given/When/Then completeness, vague terms, compound
  requirements, missing modal verbs, unfilled placeholders, and empty required sections.
- `evals/evals.json` — output-quality and triggering eval sets.

### Known gaps before release
- Owner field in `SKILL.md` frontmatter is `TBD`.
- Eval suite written but not yet run.
- Description not yet variance-tested against near-miss prompts.
