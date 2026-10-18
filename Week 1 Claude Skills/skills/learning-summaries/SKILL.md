---
name: learning-summaries
description: Writes a learning summary of a conversation and pushes it as a new row-page in the user's Notion "Lesson Summaries" database, with summary name, date, and topics covered, scaled in depth to how far the topic was explored. Use at the end of any substantial conversation in which the user investigated, explored, studied, or learned something; when the user says "summarize what we learned", "create a summary", "save this to Notion", "add this to my lesson summaries", or taps a Create summary option; and when a conversation is winding down after explaining concepts, debugging with explanation, or building something new together. Do NOT use for short factual questions, casual chat, conversations the user has said not to summarize, summaries of documents or meetings the user supplies, or course submissions that must be written without AI.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.2.0
  category: productivity
  tags: [notion, summaries, knowledge-management]
---

# Learning Summaries

The point of a learning summary is retrieval: a month from now, the user should be able to
find what they learned and pick it back up without re-reading the conversation. That shapes
every decision below — plain language over completeness, a stable structure over clever
formatting, and consistent topic tags so the table stays filterable.

The flow has two moments: **offer** at the end of a substantial conversation, and **push** when
the user accepts. The tap on "Create summary" is the user's approval; push immediately, then
show the link.

## Step 1: Offer at the end of a substantial conversation

Offer when the conversation involved real learning: a new topic explored, a concept explained,
a design reasoned through, something built and understood. Do not offer after a quick factual
answer, a one-line fix, or casual chat — an offer on every exchange trains the user to ignore
it.

Also do not offer when:
- the user has already declined a summary in this conversation,
- a summary of this same session was already pushed (offer to update it instead),
- the user is mid-task and the offer would interrupt.

**How to offer:** finish the actual answer first, then present one tappable choice with the
`ask_user_input_v0` tool — options "Create summary" and "Skip". Precede it with one short
line naming what would be summarized, so the user knows what they are approving:

> We covered Notion databases, tag drift, and how skill triggering works. Save a summary?

Where that tool is unavailable (Claude Code, the API), offer the same thing in one plain line
of text instead.

## Step 2: Draft the summary

Scale depth to how far the conversation went. The tiers and section rules are in
`references/summary-template.md` — read it before drafting, because the tier decides which
sections exist, and a deep template applied to a light conversation produces padded,
unreadable pages.

| Tier | When | Contains |
|---|---|---|
| **Light** | One topic, mostly explanation | Key concepts, takeaways |
| **Standard** | Several related topics, some hands-on | + examples, how the pieces connect |
| **Deep** | Long session, built something, real problem-solving | + code snippets, metaphors, mistakes and corrections, open questions |

Rules that apply at every tier:

- **Plain language first.** Define each term the first time it appears. A summary the user
  cannot read cold in a month has failed at its one job.
- **Summarize what was learned, not what was said.** No transcript replay, no "then we
  discussed". Organize by concept, not chronology.
- **Record what the user got wrong and corrected**, briefly and without judgment. Corrected
  misconceptions are the highest-value lines in a learning summary.
- **No invented content.** Only what actually came up in the conversation. If something was
  left unresolved, put it under open questions rather than resolving it in the summary.

**Summary name:** specific and searchable — "Notion databases vs simple tables, and tag drift",
not "Learning session" or "Notion stuff". **Summary date:** today's date.

## Step 3: Choose topic tags

Read the database's existing tags before choosing, and reuse an existing tag whenever one fits.
Tag drift ("API", "APIs", "REST APIs" as three separate tags) quietly destroys the table's
usefulness as an index, and it is cumulative — every new near-duplicate makes filtering worse.

Run the matcher rather than eyeballing similarity:

```bash
python3 scripts/match_tags.py --existing "API,Notion,Git" --proposed "APIs,notion databases,GitHub"
```

It normalizes case, plurals, and punctuation and reports which proposed topics map onto an
existing tag and which are genuinely new. Use its mapping. Aim for 2–5 tags per summary;
broader tags beat precise ones, since the summary body carries the detail.

## Step 4: Push to Notion

Database location, schema, and how to call the connector are in `references/notion-schema.md`.
In order:

1. **Find the database** inside the "Lesson Summaries" page. If it does not exist, stop and
   ask before creating it — creating the database is a one-time structural change, not part
   of an ordinary push, and the tap approved a summary, not a schema.
2. **Check for a duplicate** — a row with the same name, or the same date and overlapping
   topics. If one exists, update that page rather than creating a second. Re-running a push
   must never produce two rows for one session.
3. **Create the row-page** with the three properties and the summary as the page body.
4. **Show the link** in one line. No recap of the content — the user can open it.

If the push fails, say so plainly with the reason, and offer the summary inline so nothing is
lost. Never report success without a returned page URL.
