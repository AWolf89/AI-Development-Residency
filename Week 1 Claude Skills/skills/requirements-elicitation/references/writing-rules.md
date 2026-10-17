# Writing rules for requirements

A requirement is only useful if two people reading it build the same thing, and a third can
tell whether it was met. These rules exist to get that property.

## One requirement, one statement

Split anything joined by "and", "also", or a comma list into separate requirements. Compound
requirements get partially implemented and then argued about, because "done" is ambiguous.

- Weak: `FR-3: The system shall validate the upload and email the submitter and log the result.`
- Better: three requirements, `FR-3`, `FR-4`, `FR-5`, each independently testable.

## Make it observable

Every requirement should imply a test someone could run. If you cannot describe how to check
it, rewrite it until you can.

- Weak: `The report should load quickly.`
- Better: `The report shall render within 3 seconds at the 95th percentile for datasets up to 50,000 rows.`

## Use a consistent sentence shape

For functional behavior, the EARS forms carry their trigger condition in the sentence, which
makes gaps visible:

- Ubiquitous: *The system shall <response>.*
- Event-driven: *When <trigger>, the system shall <response>.*
- State-driven: *While <state>, the system shall <response>.*
- Conditional: *If <condition>, then the system shall <response>.*
- Optional: *Where <feature is included>, the system shall <response>.*

Mixing forms is fine; writing without any trigger condition is how error cases get lost.

## Words to replace on sight

These feel like specifications but carry no agreed meaning. Each needs a number, a name, or
a named standard:

fast, slow, quick, scalable, robust, secure, user-friendly, intuitive, simple, seamless,
flexible, efficient, reliable, appropriate, reasonable, acceptable, adequate, minimal,
optimal, best practice, industry standard, as needed, where possible, etc., and so on,
state-of-the-art, modern, clean, nice, better.

"Support" is a quiet offender too — *supports SSO* could mean one provider or every provider.
Name them.

## Say shall, should, or may deliberately

- **shall** — mandatory; absence is a defect.
- **should** — preferred; a deviation needs a stated reason.
- **may** — optional; implementer's choice.

Use them consistently, because readers will infer priority from the verb whether you intended
it or not.

## Acceptance criteria

Each functional requirement gets at least one criterion in Given/When/Then form, covering the
case that matters most. Add criteria for the significant error and boundary cases rather than
only the happy path — the happy path is the one nobody forgets to build.

```
FR-4: When a submitted file exceeds the size limit, the system shall reject it and explain why.

AC-4.1
  Given a signed-in user on the upload page
  When they submit a file larger than 25 MB
  Then the upload is rejected, no partial file is stored,
   and the message names the 25 MB limit and the file's actual size.
```

Keep criteria about observable behavior, not implementation. *Then a row is written to the
audit table* is a design decision; *Then the action appears in the user's activity history*
is a requirement.

## Describe the need, not the solution

If the requirement names a specific library, vendor, or screen layout, check whether that is
a genuine constraint or a solution that slipped in. Genuine constraints belong in the
Constraints section, where they can be reviewed as decisions.

## Mark what you inferred

Anything you supplied rather than heard goes in Assumptions, phrased so it is easy to
contradict: *"Assumed the 25 MB limit matches the existing document service; confirm with
Platform."* Assumptions buried as fact are the single most common way a spec goes wrong
quietly.

## Keep traceability intact

IDs are stable once published. When a requirement is removed, mark it withdrawn rather than
renumbering the ones after it — tests, tickets, and review comments point at those numbers.
