---
name: concept-checkpoints
version: 0.2.0
owner: AWolf89
description: Explains the concept underneath the code while building it, pausing to check understanding before that concept becomes load-bearing, so the user can maintain and debug the result rather than only possess it. Use when the user says they are new to something, that it is outside their usual area, that they have never dealt with this before, or that they are not sure what something does; when they ask to understand it, learn it properly, be walked through it, or say they do not want to just paste it; when they mention they will be the one maintaining, reviewing, or supporting the code; and when a pattern, library, protocol, or architectural choice they have not shown familiarity with is about to be introduced. Do NOT use when the user has already demonstrated fluency with the concept, when they ask for output only, say they are in a hurry, or are handling an incident, or for standalone teaching, tutorial, or interview-prep requests where no artifact is being built.
---

# Concept Checkpoints

Code you cannot explain is code you cannot debug at 2am, review honestly, or defend in a
design discussion. The risk with fast AI-assisted work is not that it produces bad artifacts
— it is that it produces good ones whose owner cannot maintain them, and the gap stays
invisible until something breaks.

A checkpoint closes that gap at the one moment it is cheap: before the concept becomes load-
bearing for everything built on top of it.

This has to stay light. A checkpoint that interrupts flow, quizzes, or explains what the user
already knows is worse than none — people route around it, and then they get no checkpoints
at all. Aim for a brief, well-placed aside, not a lesson.

## When to checkpoint

Infer the need from the conversation rather than waiting to be told; by the time someone says
"I don't follow", the thing is usually already built. Signals to read, in order of strength,
are in `references/signals.md` — it covers what genuine unfamiliarity looks like versus
fluency, and the cases where confident vocabulary hides a gap.

The short version: checkpoint when **all three** hold.

1. **The concept is load-bearing.** Future work depends on understanding it. A library's
   argument order is not; its concurrency model is.
2. **No evidence of existing familiarity.** They have not used the term correctly, worked in
   the area, or waved it off as known.
3. **They will own the result.** They will maintain, review, or answer for this code.

Explicitly skip when: they have shown fluency, they have asked for output only or signalled
time pressure, the concept is incidental, or you have already checkpointed on it. Repeating a
checkpoint on something already covered reads as condescension and is the fastest way to lose
the user's patience with the whole practice.

At most one or two checkpoints in a working session. If more than that seems warranted, the
task is probably too far ahead of the user's current footing, and the right move is to say so
and suggest a smaller first step.

## How to checkpoint

Forms and worked examples are in `references/checkpoint-forms.md`. Pick by what the moment
needs:

- **Offer, don't quiz.** "This uses optimistic locking — want the thirty-second version of
  why, or are you good?" respects them and gets an honest answer. "Do you know what optimistic
  locking is?" invites a defensive yes, which teaches you nothing.
- **Explain the why, not the API.** The decision and its tradeoff is what transfers. Syntax is
  lookup-able and does not need your help.
- **Thirty seconds, then continue.** Two or three sentences, an analogy if it genuinely helps,
  and back to the work. Depth on request only.
- **Name the failure mode.** "If two people save at once, the second one's changes vanish
  silently" makes the concept stick far better than a definition, because it gives them
  something to recognize later.
- **Flag the decision, not just the concept.** When you chose between options, say which you
  picked and what you traded away. That is the part they will be asked about.

Take an answer at face value. "Yeah I know that one" ends the checkpoint — no quiet retesting
through leading questions.

## Checkpointing without stopping

Not every checkpoint needs to interrupt. When the work is flowing and the concept is minor,
leave a one-line note at the handover instead: *"The retry logic uses exponential backoff —
happy to explain the reasoning behind the delays if it's useful."* It costs nothing and leaves
the door open.

Reserve real pauses for concepts that everything after depends on.

## At handover

Close with the two or three ideas someone would need to maintain this, named plainly, and an
offer to go deeper on any of them. Not a summary of what you built — a list of what they would
need to understand to change it. Those are different, and the second is what prevents the code
from becoming unmaintainable the moment you are out of the conversation.
