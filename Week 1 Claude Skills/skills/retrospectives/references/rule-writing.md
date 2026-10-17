# Turning a correction into a rule

Two occurrences make a candidate, not a rule. This file is the gate between them, because the
failure mode here is quiet and cumulative: a library that grows a narrow prohibition after
every incident gets steadily worse, since each one is a chance to misfire on a task that
merely resembles the original.

---

## The generalization test

A candidate becomes a proposal only if all four hold.

**1. It would fire on future, different tasks.**
Imagine three plausible upcoming tasks. Would the rule apply usefully to at least one that is
not a close replay of the original? If it only ever fires on the incident that produced it,
it is a note, not a rule.

**2. The two occurrences were genuinely independent.**
Same cause, different context. Two failures in one unusual codebase during one afternoon are
closer to one event observed twice. Independence is what makes a count meaningful at all — and
with a threshold of two, it is the main thing standing between a pattern and a coincidence.

**3. It will not misfire.**
Describe a situation where following the rule would produce a worse outcome. Every rule has
one. If the misfire case is common, narrow the rule or leave it out; if you cannot think of
one, you have not looked hard enough, and that is itself a reason to pause.

**4. Nothing already covers it.**
Check the target skill. If a rule exists and was not applied, adding another does not fix
anything — raise the application problem instead.

Failing any of these means keep logging. A third occurrence changes the evidence; restating
the same proposal does not.

---

## Where a rule belongs

Put it in the skill whose description would cause it to trigger on the situation it addresses.
Wrong placement is as bad as a wrong rule: a rule in a skill that never fires for that kind of
task is invisible, and one in a skill that fires constantly turns into noise.

- A behavior during a kind of work → that work's skill.
- Something to establish before starting → the elicitation or decomposition skill.
- Something to check before handing over → the verification or coverage skill.
- A fact about this organization's systems, standards, or vocabulary → a context skill, not a
  behavioral one. These are often mistaken for behavioral rules and then phrased as
  prohibitions, which is why they misfire.

If the right home does not exist, say so. A proposal for a new skill is legitimate, but it is
a bigger ask than amending one, and the bar is correspondingly higher.

---

## Writing the rule itself

- **State what to do, not only what to avoid.** "Ask which environment before running
  migrations" beats "don't run migrations on the wrong environment." A prohibition tells you
  nothing about the correct action.
- **Give the reason.** A rule whose purpose is explained gets applied sensibly in situations
  its author did not foresee. A bare imperative gets followed literally and wrongly.
- **Keep the scope as wide as the evidence, no wider.** If both occurrences involved database
  migrations, the rule is about migrations. Generalizing to "all irreversible operations" is a
  guess wearing a rule's clothing.
- **Name the observable trigger.** When does it apply? A rule with no clear entry condition
  either fires always or never.
- **Avoid absolutes unless the case is genuinely absolute.** "Never" rules are brittle and
  accumulate exceptions until they are ignored wholesale.

---

## The proposal format

Four elements, in a few lines:

1. **The rule**, in the words it would be written in.
2. **The evidence** — the occurrences, briefly, with enough detail to recognize them.
3. **The location** — which skill and which section.
4. **The risk** — what adopting it costs, and the situation where it would misfire.

Then stop and wait. Drafting the edit before approval presumes the answer, and the user has
context on their own library that you do not.

---

## When the answer is "no rule"

Legitimate outcomes, and worth saying explicitly rather than straining for a rule:

- **One-off.** Unusual circumstances, no general lesson.
- **Requirements problem, not a skill problem.** The fix is in how the ask is written. Hand it
  to coaching.
- **Already covered.** An existing rule was not applied. Raise that.
- **Too narrow.** The only rule that would have prevented it is so specific it is a note.
- **Cost exceeds benefit.** A minor correction recurring twice may not be worth the attention
  a permanent rule consumes.

Saying "no rule needed, here is the note" is a successful retrospective. The library's value
comes from the rules it does not contain as much as the ones it does.

---

## After a decision

- **Approved** → mark it, then make the edit as a separate, reviewable change with a changelog
  entry and a version bump.
- **Declined** → mark it declined and do not raise it again. If the same cause recurs several
  more times, that is new evidence and can be mentioned once, as new evidence rather than as
  the same proposal.
- **Deferred** → leave it as a candidate and keep logging.
