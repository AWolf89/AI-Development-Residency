# Notion database: location, schema, and push procedure

All Notion access goes through the Notion connector's tools (search, fetch, create pages). No
script talks to Notion directly: the skill's execution environment cannot reach Notion's API,
and the connector carries the user's own permissions, which is the least-privilege option
anyway.

Exact tool names and parameters vary by connector version. Load them with `tool_search` and
use the parameter names the tool returns rather than assuming them from this file.

---

## Location

- Parent page: **Lesson Summaries** (a top-level page in the user's workspace).
- The database is an inline database *inside* that page, also titled **Lesson Summaries**.

To find it: search Notion for "Lesson Summaries", fetch the page, and look for the database
and its data source in the result. Cache nothing across conversations — page IDs can change if
the user moves or duplicates the page, so look it up each time.

If the page exists but contains no database, the setup has not been done. Stop and ask before
creating it (see SKILL.md, Step 4).

---

## Schema

| Property | Notion type | Notes |
|---|---|---|
| Summary name | Title | Specific and searchable — see the name examples in the template. |
| Summary date | Date | The date of the session, ISO format (YYYY-MM-DD). Date only, no time. |
| Topics covered | Multi-select | 2–5 tags. Reuse existing options; see the tag rules below. |

These three names are the contract. If the user renames a property, use their name — read the
schema from the data source rather than assuming the names above — and mention the mismatch
once so the skill can be updated.

Do not add properties during a push. A schema change is a separate decision for the user.

---

## Creating the database (one-time setup, only with explicit approval)

Create an inline database on the Lesson Summaries page with exactly the three properties above.
Then confirm with the user that it appears as expected before pushing the first summary.

If the user has an existing standalone summary page (for example a "Session Learning Summary"
page created before this skill existed), offer to add it as the first row — do not move or
copy it without asking.

---

## Topic tag rules

1. Fetch the data source schema to get the existing multi-select options.
2. Run `scripts/match_tags.py` with the existing options and your proposed topics.
3. Use existing options wherever the script maps one. Create a new option only when the
   script reports a topic as genuinely new.
4. Prefer the broader tag. "Git" beats "Git rebase conflicts"; the body carries the detail.
5. Title Case for new tags, matching the style of existing ones if they differ.

---

## Duplicate check (before every create)

Query the database for:
- a row whose Summary name matches the proposed name (case-insensitive), or
- a row with the same Summary date whose topics overlap with at least half of the proposed
  topics.

If either matches, it is very likely this session was already summarized. Update that page's
body and topics rather than creating a new row, and say so in the confirmation line
("Updated your existing summary: …").

This is what makes the push idempotent: running it twice on one session must leave exactly
one row.

---

## Push sequence

1. Find the database (above).
2. Read existing tags → run the matcher → final tag list.
3. Duplicate check → decide create or update.
4. Create (or update) the page with the three properties and the summary as page content,
   formatted as Notion-flavored Markdown.
5. Confirm with the returned page URL as a single line.

## Failure handling

- **Connector not available or not authorized:** say so, and give the summary inline so it is
  not lost. Do not retry in a loop.
- **Page or database not found:** say exactly which one, and offer setup.
- **Create fails:** report the error message plainly, give the summary inline.
- **Never claim success without a URL from the create or update response.**
