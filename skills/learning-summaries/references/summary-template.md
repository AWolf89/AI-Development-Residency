# Summary template and depth tiers

The page body is the summary. Properties (name, date, topics) live in the database row, so do
not repeat them as a heading block at the top of the page.

Choose the tier first, then include only that tier's sections. Sections in a lower tier are
always included in higher ones.

---

## Choosing a tier

Judge by what happened, not by how long the conversation was. A long chat that circled one
idea is Light; a short one that built and debugged something is Standard or Deep.

- **Light** — one topic, mostly explanation, no hands-on work.
- **Standard** — several related topics, or one topic with examples and some hands-on work.
- **Deep** — something was built, debugged, or designed; multiple misconceptions were
  corrected; or the session covered enough that the user will genuinely need to come back to it.

When torn between two tiers, choose the lighter one. A short summary that gets reread beats a
long one that does not.

---

## Light

```markdown
## In one sentence
<What this was about and the single most important thing learned.>

## Key concepts
- **<Term>** — <plain-language definition, one or two sentences.>
- **<Term>** — <…>

## Takeaways
- <What to remember or do differently.>
```

3–5 key concepts at most. If there are more, it is probably Standard.

## Standard — adds

```markdown
## How it fits together
<A short paragraph connecting the concepts: which depends on which, and why it matters.>

## Examples
- <Concrete example from the conversation, in a sentence or two.>
```

## Deep — adds

```markdown
## Mental model
<A metaphor or analogy that captures the core idea, followed by where the metaphor breaks
down. Never give a metaphor without its limit — an unbounded metaphor becomes a wrong model.>

## Code and commands
<Only snippets the user will actually reuse. Each with one line saying what it does.>

## What I got wrong at first
- <Misconception> → <what is actually true.>

## Open questions
- <Anything left unresolved, to pick up next time.>
```

---

## Writing rules

- **Define on first use.** Every technical term gets a plain-language definition the first
  time it appears.
- **Concept order, not chronological order.** "First we talked about X, then Y" is a
  transcript, not a summary.
- **Second person is fine, first person for the learner's own mistakes.** "What I got wrong"
  reads as the user's own notes, which is what these are.
- **No filler.** No "In this session we explored…" preamble, no closing paragraph.
- **Nothing invented.** If it did not come up, it does not go in. Unresolved items go under
  open questions, not into a confident answer the conversation never reached.
- **Code fences carry a language tag** so Notion highlights them.

---

## Name examples

| Weak | Better |
|---|---|
| Learning session | Notion databases vs simple tables, and tag drift |
| Python stuff | Python virtual environments and why pip installs go global |
| Git | Rebasing vs merging, and recovering a bad rebase |
| Skills | How Claude skill descriptions decide when a skill triggers |

A good name is what the user would type into search a month from now.
