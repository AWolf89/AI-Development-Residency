# Question banks

Contents:
1. Universal core — ask on every elicitation
2. Software features and applications
3. Data, integrations, and pipelines
4. Automation and internal tooling
5. Probes for when answers stay vague

Select from these rather than asking all of them. In a light interview you may only need the
core. Phrase them in the requester's own vocabulary, not this document's.

---

## 1. Universal core

Ask these in roughly this order. The sequence matters: problem before solution, users before
features, boundaries before detail.

**Problem**
- What breaks or costs you today that this is meant to fix?
- How are people handling it now? (Workarounds reveal real requirements.)
- What happens if we do nothing for six months?
- Why now — what changed?

**Users and stakeholders**
- Who uses this directly, and how often? Daily, or twice a year?
- Who else is affected but never touches it? (Approvers, auditors, downstream teams.)
- What do they know and expect? A support agent and an external customer need different things.
- Who can say no to this?

**Scope**
- What is explicitly not part of this?
- Is anything being replaced or retired, or does this run alongside what exists?
- What is the smallest version that would still be worth shipping?
- Which parts are fixed requirements and which are preferences?

**Success**
- How will you know this worked? What would you measure a month after launch?
- What would make you call it a failure even if it technically functions?

**Constraints**
- Any deadline, and what is driving it?
- Any technology, vendor, or platform that is mandated or forbidden?
- What budget, headcount, or skills limits apply?
- Any policy, contractual, or regulatory requirement in play?

**Failure and edges**
- What should happen when a required input is missing or malformed?
- What does the empty state look like — day one, no data?
- What happens at 10x the expected volume?
- If this fails midway, what state should things be left in?
- Who gets notified when something goes wrong?

---

## 2. Software features and applications

- Walk me through the flow as the user experiences it, start to finish.
- Where does the user enter this flow from, and where do they land after?
- What can they do wrong, and what should happen when they do?
- Which actions are reversible? Which need confirmation?
- What should different roles see and be able to do?
- Does this need to work on mobile, offline, or in a specific browser?
- What accessibility expectations apply?
- Any localization or multi-currency needs?
- What should an existing user with existing data see on first use of this?
- Does anything need to be logged for audit or support?

## 3. Data, integrations, and pipelines

- Where does the data come from, and who owns that source?
- What is the schema today, and how often does it change without warning?
- How fresh does it need to be — real time, hourly, next day?
- What volume, and how fast is it growing?
- What makes a record valid? What should happen to invalid ones — reject, quarantine, or pass through flagged?
- Can records arrive duplicated, late, or out of order?
- Is this a one-time load, incremental, or full refresh?
- What happens when the upstream system is down or rate limited?
- Can this be re-run safely after a partial failure?
- Does any of this contain personal, financial, or regulated data? What retention and deletion rules apply?
- Who consumes the output, and what breaks for them if the shape changes?
- How will we know the data is wrong rather than just absent?

## 4. Automation and internal tooling

- What is the manual process today, step by step, including the informal bits?
- Which steps genuinely need a human decision, and which are mechanical?
- What triggers it — schedule, event, or someone pressing a button?
- What does it touch that cannot be undone? (Sending, publishing, paying, deleting.)
- What should it do when it hits a case it was not designed for — stop, skip, or escalate?
- Who needs to see that it ran, and that it ran correctly?
- What happens when the person who owns this is on leave?
- If it runs twice by accident, what is the damage?
- Does it need an off switch, and who is allowed to use it?

---

## 5. Probes for when answers stay vague

Use these to convert a placeholder answer into a requirement:

| They say | Ask |
|---|---|
| "It should be fast" | What's the slowest it could be before someone complains? Measured where? |
| "It should be secure" | Who are we protecting this from, and what would they be after? |
| "Handle errors gracefully" | Show me a specific error — what should the user see, and what should we do? |
| "It should scale" | To what number, by when? |
| "Like the old system" | Which parts of the old system do people actually like? |
| "Everyone uses it" | Can you name the three groups who use it most differently? |
| "It's simple" | What's the trickiest case you can think of? |
| "Obviously it should…" | Obvious to you — say it out loud so I can write it down. |
