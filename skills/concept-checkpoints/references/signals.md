# Reading the signals

Inferring unfamiliarity is a judgment call made on thin evidence, and it fails in both
directions: checkpointing someone fluent is patronizing, missing someone lost leaves them with
unmaintainable code. These are the signals worth weighting.

---

## Signals of a gap

**Strong**
- They ask what something is, or ask you to explain a term you used.
- They describe the goal in outcome terms with no mechanism: "I need users to stay logged in"
  rather than "I need refresh token rotation".
- They accept a significant design decision without engaging with the tradeoff.
- They say they are new to the area, learning it, or that it is outside their usual work.
- They ask whether something is "the right way", which usually means they cannot yet judge.

**Moderate**
- Vocabulary used loosely or interchangeably when the distinction matters — async and
  parallel, authentication and authorization, index and key.
- They copy a suggestion verbatim without adapting obvious parts to their context.
- Their questions are all about whether it works, never about why it is built that way.
- They ask for something that implies a misconception, like wanting a cache that is always
  perfectly fresh.

**Weak on its own, meaningful in combination**
- Unusual silence after a dense explanation.
- Agreement that arrives faster than reading time.
- Repeating your phrasing back without rewording it.

---

## Signals of existing fluency — skip the checkpoint

- Correct use of the vocabulary, including the distinctions non-experts blur.
- They name the tradeoff themselves, or ask about the failure case before you raise it.
- They push back on a design choice with a specific reason.
- They mention having built, operated, or debugged something similar.
- They supply their own constraints ("we need this idempotent, retries are at-least-once").
- Their questions are about your specific choice rather than about the concept generally.

Fluency in one area says little about the next. Someone deeply fluent in databases may be new
to frontend state management. Read signals per concept, not per person, and do not let an
early impression of expertise suppress a checkpoint in a different domain.

---

## The hard case: confident vocabulary over a shaky model

The riskiest situation is someone using terms correctly while holding a wrong model
underneath, because every surface signal reads as fluency.

Tells worth noticing:
- The term is used correctly but always in the same phrasing, never reworded or applied to a
  new case.
- They know what it does but not what it costs or when it fails.
- They can name the pattern but not why it was chosen over the alternative.

Handle it by talking about the decision rather than the term: *"I went with eventual
consistency here because the write volume makes the alternative expensive — does that match
how you'd expect this to behave under load?"* That invites engagement with the model without
testing them on a definition, so there is no face to lose in saying "actually, no".

---

## Weighing it up

Checkpoint when the concept is load-bearing and the signals lean toward a gap. When the
evidence is genuinely balanced, the low-cost move is the offer form — "want the short version
of why this works this way?" — which costs one line and lets them decide. That is the right
default under uncertainty, and it means you rarely need to be confident about the inference
at all.

What to avoid in both directions: assuming a gap because the task is simple (experts ask
simple questions), and assuming fluency because someone is senior, technical, or using the
right words.
