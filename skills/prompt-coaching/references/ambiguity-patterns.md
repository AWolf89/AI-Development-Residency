# Ambiguity patterns

The recurring shapes of ambiguity, each with what it forces you to guess and the wording that
removes the guess. Use the category names consistently when logging, so repeats are countable.

---

## `undefined-term`

A word doing heavy lifting with no shared definition — usually a comparative or a domain term
used loosely.

- "make it faster", "clean this up", "handle errors properly", "make it production-ready"
- "active users", "recent", "large file", "soon"

**Guess forced:** which dimension, and what threshold counts as success.

**Closes it:** a number, a baseline, or a named standard. *"Cut the p95 load time below 2s"*;
*"active = logged in within 30 days"*.

## `unstated-scope`

The change is clear; its boundary is not.

- "add validation to the form" — this form, or every form?
- "fix the export bug" — this symptom, or the class of bug?
- "update the docs" — the page you changed, or everywhere it is mentioned?

**Guess forced:** how far to reach.

**Closes it:** name the files, the surfaces, or the stopping point. *"Just the checkout form,
leave the others"*.

## `missing-success-criteria`

No statement of what finished looks like, so completion is a judgment call.

- "improve the onboarding flow"
- "write some tests for this"

**Guess forced:** when to stop and what good means.

**Closes it:** the observable end state. *"Tests covering the three failure paths in the
payment handler"*.

## `implied-constraint`

A constraint that exists in the user's head and nowhere in the request — a library they will
not accept, a pattern the team banned, a deadline, a system that must not change.

**Guess forced:** which approaches are actually available.

**Closes it:** state the non-negotiables up front. *"Stick to the standard library"*; *"don't
touch the shared auth module"*. Constraints are cheaper to state than to discover in review.

## `ambiguous-referent`

Pronouns and demonstratives with more than one candidate: "it", "this", "that one", "the
file", "the other approach".

**Guess forced:** which thing.

**Closes it:** name it once. In longer threads, names beat pronouns even when it feels
repetitive.

## `unstated-audience`

Who the output is for, which determines register, depth, and format more than anything else.

- "write up what we did" — for your team, your manager, or a customer?
- "explain this" — to you, or for you to forward?

**Guess forced:** tone, length, and assumed knowledge.

**Closes it:** one phrase. *"for our CTO, who knows the system"*; *"for a customer-facing
release note"*.

## `unstated-format`

Deliverable shape left open: a file or a reply, prose or a table, a patch or a full file, one
document or several.

**Guess forced:** shape, which often means rework when wrong.

**Closes it:** name it. *"as a markdown file I can paste into Confluence"*.

## `conflicting-statements`

Two requirements that cannot both hold, usually from different parts of a thread or different
stakeholders.

- "keep it simple" alongside a list of twelve configuration options.
- "don't change the API" alongside a change that requires a new field.

**Guess forced:** which one wins.

**Closes it:** rank them, or say which is the hard constraint. Worth raising during the work
rather than only in feedback — conflicts usually need a decision, not an assumption.

## `example-as-specification`

A single example standing in for the rule, leaving the general case open.

- "like the invoice export, but for orders" — which aspects carry over?
- "name them like `user_id`" — a convention, or just that one?

**Guess forced:** which properties of the example are the requirement.

**Closes it:** say what generalizes. *"Same column layout and filename pattern; different
filters"*.

## `missing-context`

The information exists but was not shared: the error text, the file, the previous attempt,
the constraint discovered last week.

**Guess forced:** the circumstances, often reconstructed wrongly.

**Closes it:** paste the error, attach the file, link the thread. The single highest-value
addition to most requests.

---

## Using these in feedback

Name the pattern in plain words, not by category label — "who this is for" rather than
"`unstated-audience`". The labels exist for counting repeats in the log, not for talking to
people.

And weigh before mentioning: ambiguity you resolved correctly and cheaply is not worth
raising. The ones worth a line are those that could plausibly have gone the other way, or did.
