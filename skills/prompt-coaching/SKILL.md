---
name: prompt-coaching
version: 0.2.0
owner: AWolf89
description: Gives brief, concrete feedback on where a request was ambiguous, naming each point at which an assumption had to be made, what was assumed, and the wording that would have removed the guess, so the user's prompts and written requirements get sharper over time. Use when the user says that is not what they meant, asks why it was built or written that way, asks whether their request or instructions were clear, asks where they were vague or unclear, asks how to phrase or word their asks better, notes that they keep going back and forth or repeating themselves, or asks for feedback on their own prompt; and after completing a substantial task in which assumptions had to be made. Do NOT use for trivial or conversational exchanges, when the request was already unambiguous, when the user has declined this feedback, for reviewing a requirements document written for others, or for general prompt-engineering guides, training material, or writing-style critique.
---

# Prompt and Requirements Coaching

Every ambiguous request gets resolved somehow. If nobody says how, the user never learns
which part of their wording forced the guess — and writes the same shape of request next
time. A short, specific note at the end closes that loop, and the skill transfers directly to
written requirements, where the same ambiguity costs far more.

Two things make this work or fail. **It must be grounded in guesses actually made during this
task** — invented or generic advice ("be more specific") is noise, and people stop reading it.
And **it never substitutes for asking during the work**: if ambiguity is blocking you, ask
then. Coaching covers the assumptions that were reasonable to make and worth surfacing, not
questions you should have raised and did not.

## Step 1: Notice guesses while working

Keep a running note of each point where the request did not determine your choice: what you
assumed, and what in the wording left it open. Reconstructing afterward produces vague
feedback, because by then your assumption feels like the obvious reading.

The categories worth watching — undefined terms, unstated scope, missing success criteria,
implied constraints, ambiguous pronouns and referents, unstated audience, conflicting
statements — are in `references/ambiguity-patterns.md`, with the before-and-after wording for
each.

## Step 2: Give the feedback

After a substantial task, add a short section at the end. Two to four points, the ones that
actually mattered. If nothing was genuinely ambiguous, say nothing — a note on every task
regardless of content trains people to skip it.

Use this shape, since it carries the three things that make feedback actionable: where the
gap was, what you did about it, and the concrete wording that would have closed it.

```
**On the request itself**

- "<the ambiguous phrase>" — I assumed <assumption>. If you meant <alternative>,
  <specific rewording> would have settled it.
```

A worked example:

> - "make it faster" — I optimized the database queries, since that was the bottleneck in the
>   profiler. If you meant perceived speed for the user, adding something like "the list page
>   should feel responsive while loading" would have pointed me at pagination instead.

What makes that useful: it names the exact phrase, states the assumption as a choice rather
than a reading of their mind, and supplies wording they can reuse.

## Step 3: Keep it proportionate

The tone that works is a colleague mentioning what tripped them up, not a review of the user's
writing. `references/feedback-style.md` has the phrasings that land and the ones that grate.

The rules that matter most:

- **Own the guess.** "I assumed X" places the uncertainty with you, which is accurate — the
  same words might be unambiguous in a context you lack.
- **Lead with what was clear** when there is something genuinely well-specified. It is honest
  feedback, not a compliment sandwich, and it tells them what to keep doing.
- **Never imply the request was bad.** Most ambiguity is the normal cost of writing quickly.
  The point is which specific additions pay off, not that the user should have written more.
- **Cap it.** Two to four points. A long list reads as criticism however it is phrased, and
  the marginal point teaches less than the first one does.
- **Skip what did not matter.** Ambiguity you resolved correctly and trivially is not worth
  the user's attention.

## Step 4: Surface recurring patterns

One-off notes teach less than a pattern seen three times. Log each coaching point and check
for repeats:

```bash
python3 scripts/log_ambiguity.py --add --category <category> --phrase "<phrase>" --task "<task>"
python3 scripts/log_ambiguity.py --report
```

Counting across tasks is exactly the kind of thing worth doing mechanically rather than by
impression — recency bias makes the last thing feel like the pattern. When a category recurs,
raise it once as a pattern rather than repeating the per-task note:

> Across the last several tasks, the thing that most often needs a guess is who the output is
> for. Naming the audience up front would remove most of it.

Raise a pattern at most once every several tasks. The point is a sharper collaborator, not a
running critique.

## What this is not

Not a style review of the user's writing, not a demand for formal specs on casual requests,
and not a reason to withhold work until a request is perfect. Do the task well first; coaching
is the short note at the end.
