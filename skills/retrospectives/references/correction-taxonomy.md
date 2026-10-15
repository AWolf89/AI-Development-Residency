# What counts as a correction

Counting the wrong things is how this skill fails. Log ordinary iteration and the threshold
trips constantly, producing rules nobody wanted. Log nothing unless it was a disaster and
real patterns never surface.

The test: **did the user have to tell you something you should have known or asked, in order
to get the work back on track?**

---

## Real corrections — log these

**`wrong-assumption`** — you filled a gap and filled it wrong. "No, the export is for
external customers, not internal staff."
Cause to record: the specific assumption, and what would have revealed it.

**`missed-requirement`** — something asked for was not delivered, and the user had to point
at it.
Cause: how it was lost — not in the decomposition, dropped mid-work, or misread.

**`ignored-instruction`** — an instruction was given and not applied. The most serious
category, because the information was present and unused.
Cause: where in the conversation it was given and why it did not carry.

**`scope-overreach`** — you did more than was asked and the user pushed back.

**`wrong-approach`** — the method was unsuitable and the work had to be redone, not just
adjusted.

**`unasked-question`** — you guessed where you should have asked, and the guess cost rework.
Distinct from a guess that happened to be right, which belongs in coaching, not here.

**`quality-miss`** — output was wrong, broken, or unverified in a way the user had to catch:
code that did not run, a claim that was not checked, a number that was wrong.

**`format-miss`** — the deliverable's shape was wrong enough to need redoing. A minor tweak
does not count.

---

## Not corrections — do not log

- **Refinement.** "Make it shorter", "try a warmer tone", "use a table instead." The work was
  right and the user is converging on what they want. This is the normal shape of
  collaboration.
- **Changed mind.** "Actually, let's do it the other way." New information or a new
  preference, not an error.
- **New requirements.** "Can it also handle XLSX?" Addition, not correction.
- **Genuine ambiguity the user acknowledges.** If they say "my fault, I wasn't clear", that
  belongs in prompt coaching. Logging it here would generate a rule aimed at the wrong target.
- **Exploration.** In prototyping, discarded attempts are the method working, not failing.
- **Preference differences.** They would have written it differently. That is not a defect
  unless it violates a stated standard.

When unsure, ask whether a rule could plausibly have prevented it. If no rule would have
helped, it is not a correction for these purposes.

---

## Finding the cause, not the symptom

The cause determines whether a rule is even the right fix, so it is worth a moment's thought
rather than restating what happened.

| Symptom | Possible cause | Right fix |
|---|---|---|
| Used the wrong data source | Did not ask which of three was current | Ask-earlier rule |
| Export missed a column | Requirement buried in a long message | Decomposition rule |
| Touched an unrelated file | No boundary declared before starting | Existing rule, not applied |
| Code did not run | Claimed done without executing | Verification rule |
| Wrong tone in a document | Audience never established | Requirements practice, not a skill rule |

Note the third row. When an existing rule covers it and was not applied, adding a second rule
makes things worse — the problem is application, not coverage. Record it as
`existing-rule-not-applied` and raise it as that, since the fix is usually that the rule is
buried, vague, or in a skill that did not trigger.

---

## Severity

Record roughly how much it cost, because it changes how a proposal should be weighed:

- **minor** — corrected in one exchange, no rework.
- **moderate** — required redoing a portion of the work.
- **major** — invalidated the approach, or would have caused real damage if undetected.

A major correction is worth proposing a rule for sooner. A minor one recurring twice may still
be better left as a note — the rule would cost more attention than the mistake does.
