# Decomposing a request into traceable requirements

The extractor handles structure. This file covers the judgment it cannot make.

Contents:
1. What counts as a requirement
2. Splitting compound items
3. Implied and derived requirements
4. Acceptance criteria and parent requirements
5. Material that is not a requirement
6. Unstructured sources: tickets, emails, chat threads
7. Granularity

---

## 1. What counts as a requirement

Anything that could be delivered or not delivered, and whose absence the requester would
object to. That includes obligations ("must export to CSV"), constraints ("cannot use a new
vendor"), and quality expectations ("under 2 seconds"), but not rationale or background.

A useful test: could you write a sentence beginning "this was not done because…" and would
the requester care? If yes, it is a requirement and needs a row.

## 2. Splitting compound items

Split on anything that permits partial delivery.

Source: *"Add an export button that produces CSV and XLSX, emails it to the user, and logs
the request for audit."*

Decomposes to four:
- R-1 Export button produces CSV
- R-2 Export button produces XLSX
- R-3 Completed export is emailed to the requesting user
- R-4 Export requests are recorded in the audit log

Keeping that as one row lets three-quarters of it count as done. The giveaway words are
*and*, *also*, *plus*, *as well as*, and comma lists of nouns or verbs.

Do not split what cannot be partially delivered. *"The form shall accept a date and time"*
is one requirement if the field is a single datetime, two if they are separate inputs. When
unsure, split — an over-split list costs a few extra rows, while an under-split one hides
gaps.

## 3. Implied and derived requirements

Requesters state the novel part and assume the rest. Common implications worth surfacing:

| Stated | Usually implies |
|---|---|
| Add a field | Display, input validation, persistence, inclusion in existing exports |
| New endpoint | Authentication, authorization, error responses, rate limits |
| Import data | Validation, duplicate handling, failure reporting, re-run behavior |
| Send a notification | Opt-out, failure retry, what happens when the address is invalid |
| New user-facing screen | Empty state, error state, permissions, mobile behavior |
| Delete something | Soft or hard delete, cascade, audit record, recovery |

Record these as derived requirements with `source: derived` and a note naming your inference.
Marking them keeps the honesty of the list intact: the requester can strike what they do not
want, which is far cheaper than discovering a missing assumption after delivery.

Do not invent scope. A derived requirement follows necessarily from what was asked; a feature
you think would be nice does not. If you are adding capability rather than completing it,
that belongs in a suggestion, not the trace.

## 4. Acceptance criteria and parent requirements

When the source has acceptance criteria under a requirement, keep the parent as the traceable
unit and attach the criteria to it. The parent is `met` only when every criterion passes.
Flattening criteria into peer requirements inflates the count and makes the report read as
more thorough than it is.

Exception: if a criterion describes behavior the parent does not mention at all, it is a
requirement in its own right and the source document has a gap worth raising.

## 5. Material that is not a requirement

Leave these out of the numbered list, and say so if the omission might surprise:

- Background, rationale, and problem description.
- Examples given to illustrate a requirement already captured.
- Options the requester explicitly rejected.
- Anything stated as out of scope — though it is worth echoing out-of-scope items in the
  report preamble, since "you didn't build X" is a predictable question.
- Open questions. These are not deliverable; carry them separately so they do not inflate
  the coverage denominator.

## 6. Unstructured sources: tickets, emails, chat threads

Real requests arrive as prose with the requirements scattered through them. Read the whole
thing first, then extract, because the last paragraph frequently qualifies the first.

Watch for:
- Requirements buried in asides: *"obviously it needs to work for the EU tenants too"*.
- Soft phrasing that is actually mandatory: *"it would be good if…"* from the person who
  signs off usually means *shall*. Capture it, mark the ambiguity, and ask.
- Contradictions across a thread. Later statements usually win, but confirm rather than
  assume; record the superseded version so the change is visible.
- Attachments and links referenced in passing — their contents often carry requirements.

## 7. Granularity

Aim for requirements that one person could deliver and verify in a sitting. Too coarse
("rebuild the reporting module") hides everything inside it; too fine ("add a comma") makes
the report unreadable and buries the significant items among trivia.

If a requirement would take more than a day of work to satisfy, it probably decomposes
further. If a dozen requirements all resolve together in one small change, they were probably
one requirement with detail attached.
