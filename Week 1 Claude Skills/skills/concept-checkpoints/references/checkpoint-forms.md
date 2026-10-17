# Checkpoint forms

Four forms, ordered from lightest to heaviest. Default to the lightest that fits — the cost
of a checkpoint is the interruption, so spend it carefully.

---

## 1. The flag (one line, no pause)

Name the concept and move on. Use when it is worth knowing the term exists but nothing
depends on understanding it now.

> Using a connection pool here so we're not opening a socket per request.

No question, no pause. If they want more they will ask.

## 2. The offer (one line, invites a pause)

Name it and offer the explanation. The default form under uncertainty: cheap, and it hands
the decision to them.

> This relies on idempotency keys — want the short version of why, or shall I keep going?

Why the phrasing matters: "do you know X?" pressures a yes, because admitting otherwise feels
like a confession. "Want the short version?" makes accepting costless — people take it
readily, and a declined offer is genuine information rather than face-saving.

## 3. The short explanation (two to four sentences)

Give it unprompted when the concept is load-bearing and the signals point to a gap. Structure
that works:

1. What problem it solves.
2. How it solves it, in one sentence.
3. What it costs or when it fails.

> Optimistic locking: instead of locking the row while someone edits, we let both of them
> edit and check at save time whether the version changed. It keeps things fast when
> conflicts are rare, but it means the second person to save gets an error rather than
> silently overwriting. That tradeoff is the right one here because two people editing the
> same invoice is unusual.

The failure case is the part that sticks, because it gives them something recognizable later.

## 4. The decision checkpoint (explanation plus a real choice)

Use when you made a judgment call they should own. Present the alternative honestly, say
which you chose and why, and leave the decision open.

> I can do this two ways. Store the computed total on the order — fast reads, but it goes
> stale if a line item changes and someone forgets to recompute. Or compute it on read —
> always correct, slower on big orders, and it shows up as latency on the list page. I'd lean
> to computing on read until the list page actually feels slow. Does that fit how you'd expect
> this to be used?

This is the heaviest form and the most valuable: the user ends up having made the decision,
which is the strongest version of understanding it.

---

## Phrasings that undermine the checkpoint

| Avoid | Why | Use instead |
|---|---|---|
| "Do you know what X is?" | Pressures a defensive yes | "Want the short version of X?" |
| "As you probably know…" | Makes asking feel like failure | "Quick note on why this is X…" |
| "This is pretty basic, but…" | Insulting either way | Just explain it |
| "Make sense?" after a wall of text | Only ever gets "yes" | Ask about a specific implication |
| "Let me explain how X works" (unasked, at length) | A lecture, not a checkpoint | Offer first |
| Re-explaining something already covered | Reads as not listening | Reference it: "same locking idea as before" |

---

## Checking that it landed, without testing

Avoid quizzing. Ask about application instead, where the answer is useful to the work:

- "Where else in your system would this same problem show up?"
- "Does that match how you'd expect it to behave if the job retries?"
- "Anything about that tradeoff that doesn't fit your situation?"

These are real questions — the user's answer frequently changes the design, because they know
their context better than you do. That is what makes them non-condescending: you are not
checking them, you are asking them.

---

## At handover

Two or three ideas, named plainly, with an open offer:

> To maintain this you'd mainly need: the retry/backoff behavior in `worker.py`, why the
> totals are computed on read rather than stored, and how the idempotency key prevents
> duplicate charges. Happy to go deeper on any of them.

This is not a summary of what you built. It is the list of things someone would need to
understand in order to change it safely — which is the thing that actually prevents the code
from becoming a black box when you are no longer in the conversation.
