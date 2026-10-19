# Test plan template

Keep these `##` headings exactly; the checker relies on them.

```markdown
# Test plan: <Feature name>

Status: Draft | Approved (date)
Size: Medium | New app
Design: docs/design/<name>.md (if any)

## Project choices
- Framework: <choice and why>
- External services: <mock / test copy per service, and why>

## Critical paths
Each must reach 100 percent coverage.
- <path>: <why it is critical>

## Unit tests
- <behaviour to test>: <what passing proves>

## Integration tests
- <behaviour>: <which parts work together>

## End-to-end tests
New apps only; write "Not required (medium)" otherwise.
- <user journey>

## Edge cases and errors
- <empty, invalid, duplicate, too large, service down...>

## Kanban cards
- **<Card title>:** one-line description
```
