# Checklist items

Short checklist (tiny tasks): Correctness, Security basics, Scope.
Full checklist (medium and new apps): all 8 areas.
Never N/A: Security basics, Scope.

## Correctness
- All tests pass (show the command output).
- Edge cases from the test plan are covered.
- Behaviour matches the approved design or plan, if there was one.

## Security basics
- No secrets, keys, or passwords in code or config committed to the repo.
- All user input is validated before use.
- No SQL, shell commands, or HTML built by joining strings with user input.
(Deep checks belong to the security-review skill.)

## Error handling
- Each rule in references/standards.md, "Error handling" section.

## Logging
- Each rule in references/standards.md, "Logging" section.

## Readability
- Names say what things are or do.
- No dead or commented-out code.
- Comments explain why, not what.

## Docs
- README updated for any change in setup, usage, or behaviour.
- Other docs (setup guide, API docs, diagrams, ADRs) updated where relevant.

## Scope
- Only the requested changes; no extra features, refactors, or renames.
- Anything else noticed is listed under Observations.

## Dependencies
- Each new package is needed (not easily done without it).
- Version is pinned.
- Package is actively maintained (recent releases, not deprecated) - verify, don't assume.
