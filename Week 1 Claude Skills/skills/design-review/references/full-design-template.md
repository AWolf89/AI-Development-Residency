# Full design template (new apps)

Keep these eight `##` headings exactly, in this order, followed by the Kanban cards list.
Fill every section; write "None identified yet" rather than deleting one.

```markdown
# Design: <App name>

Status: Draft | Approved (date)
Size: New app

## Problem statement
What problem this solves, for whom, and what "done" looks like.

## Components
Each part of the system and its single job.

## Data flow
How data moves between components, step by step. Include the Mermaid diagram here.

## Tech choices
For each choice:
- **Choice:** what we picked
- **Why:** plain-language reason
- **Alternative considered:** and why not
- **Analogy:** a comparison to something familiar
- **ADR:** docs/adr/NNNN-title.md

## Security considerations
Secrets, authentication, user input, data exposure. Public users means assume hostile input.

## Testing approach
What kinds of tests are needed (detailed planning happens in test-planning).

## Deployment
Local Docker for development; where and how it deploys publicly.

## Open questions
Unresolved items and who decides each.

## Kanban cards
- **<Card title>:** one-line description
```
