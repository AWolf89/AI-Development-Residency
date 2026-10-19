---
name: design-review
description: Sizes every build task as tiny, medium, or new app, then produces the matching design step before any code is written - nothing for tiny tasks, a one-paragraph plan for medium ones, and a full design document with a Mermaid diagram and an ADR for new apps - and waits for an explicit "approved" before building. Use whenever the user asks to build, create, add, or start something, such as a new app, service, repo, feature, integration, API, or n8n workflow, or says "plan this", "design this", "how should we build", or "architecture". Also use when a build already underway needs to change its plan. Do NOT use for answering questions, explaining concepts, fixing a typo or one-line bug, reviewing finished code, or redesigning an existing app the user has not asked to redesign.
license: MIT
compatibility: Works in Claude Code, Claude.ai, and the API. Writing docs needs file access to the repo; creating Kanban cards needs a connected Notion tool.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.1.0
  category: engineering
  tags:
  - design
  - architecture
  - adr
  - planning
---

# Design Review

Code written before the plan is agreed gets rewritten. This skill puts a design step in
front of building, sized so small jobs stay fast and big ones get real thought. The user
is learning, so every design also teaches: tech choices come with plain-language reasons.

## Critical rules

1. **No code before approval.** Not a scaffold, not a "quick start". Writing design files
   in `docs/` is allowed; application code is not.
2. **Only an explicit "approved" counts as sign-off.** "Looks good", "sure", or "ok" are
   feedback: ask "Reply 'approved' to start building, or tell me what to change."
3. **Any change to an approved plan stops the build.** Describe the change and why, update
   the design, and wait for a new "approved". This applies to every change, however small.
4. **Never redesign an existing app** unless the user asked for a redesign.

## Step 1: Size the task and say so

| Size | Signals | Design step |
|---|---|---|
| Tiny | One file, easy to undo | None |
| Medium | Several files, or a new feature | One-paragraph plan |
| New app | New repo or new service | Full design + Mermaid diagram + ADR |

Always open with the size and one-line reason, and let the user override before doing
anything else: *"This adds a new service, so I'm treating it as a new app (full design).
Want a different size?"* If signals are mixed, pick the larger size.

Tiny tasks: state the size, wait for no-objection or an override, then proceed normally.
This skill does nothing more for them.

## Step 2: Write the design

- **Medium:** use `references/medium-plan-template.md`. Each tech choice gets a one-line
  plain-language reason.
- **New app:** use `references/full-design-template.md` and keep all eight sections in the
  exact order and names given (the checker relies on them). Each tech choice gets a
  plain-language explanation, the alternative considered, and an analogy. Include one
  Mermaid diagram (see `references/mermaid-guide.md`). Write an ADR from
  `references/adr-template.md` for each significant tech choice.

File locations (create folders if missing):
- Full design: `docs/design/<kebab-case-name>.md`
- ADRs: `docs/adr/NNNN-<kebab-case-title>.md` - get the number from
  `python3 scripts/next_adr.py docs/adr` rather than counting by eye.
- Medium plans stay in the chat; do not write a file for them.

Before presenting a full design, run:

```bash
python3 scripts/check_design.py docs/design/<name>.md
```

Exit code 0 means all sections, the diagram, and the Kanban list are present. Fix anything
it reports before showing the design.

## Step 3: List the Kanban cards in the design

Every medium plan and full design ends with a **Kanban cards** list: one card per
buildable piece of work, each with a short title and one-line description. The user's
"approved" covers both the design and these cards, so the cards are confirmed before they
are created.

## Step 4: Get sign-off

Present the design and end with: *"Reply 'approved' to approve the design and create the
cards listed above, or tell me what to change."* Revise and re-present until approved.

## Step 5: After "approved"

1. Create the listed cards in the Notion database **AI Dev Project Kanban Board**, in the
   **Backlog** column. Details and failure handling: `references/notion-kanban.md`.
2. Report what was created (titles and links).
3. Suggest the test-planning skill as the next step. Do not start it without the user.
4. Then build to the approved design.

## Examples

**New app.** User: "Let's build a public API that shortens URLs."
Actions: state "New app (new service), full design - override?"; write
`docs/design/url-shortener.md` with all eight sections, a Mermaid diagram, and three
Kanban cards; write `docs/adr/0001-use-postgres.md`; run the checker; ask for "approved".
On "approved": create the three Backlog cards, report them, suggest test-planning.

**Medium.** User: "Add email notifications to my n8n workflow."
Actions: state "Medium (several nodes, new feature) - override?"; give a one-paragraph
plan with one-line reasons and a cards list; wait for "approved".

**Tiny.** User: "Rename this variable."
Actions: "Tiny (one file, easy to undo), no design step - override?" then proceed.

**Mid-build change.** While building, a queue turns out to be needed.
Actions: stop, explain the change and why, update the design and ADR, ask for a new
"approved" before continuing.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| User says "looks good" | Not explicit sign-off | Ask for "approved"; do not build |
| `check_design.py` reports a missing section | Heading renamed or dropped | Restore the exact heading from the template |
| User disputes the size | Signals were ambiguous | Use their size; no argument needed |
| Notion tool unavailable or board not found | Not connected, or board renamed | Do not build silently past it: tell the user, show the card list so it can be added by hand, and continue only if they say so |
| Card with the same title already in Backlog | Re-run after a partial failure | Skip it; never create duplicates |
| No repo or file access (e.g. Claude.ai chat) | Surface limitation | Present the design and ADR in chat and say which paths they belong at |

## Where this skill stops

It plans and gets sign-off. It does not write tests (test-planning does), review code, or
create anything beyond the design files and the approved cards.
