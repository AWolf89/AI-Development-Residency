# Creating Kanban cards in Notion

Target: database **AI Dev Project Kanban Board**, column **Backlog**.

1. Search Notion for the database by its exact name. If several match or none do, stop
   and ask the user; do not guess.
2. Fetch the database schema to find the status/column property and confirm a "Backlog"
   option exists. If it does not, stop and ask.
3. Query existing Backlog cards. Skip any listed card whose title already exists, so a
   re-run never duplicates (idempotent).
4. Create each remaining card: title from the list, description in the page body,
   column set to Backlog.
5. Report created and skipped cards with links.

Only create the cards listed in the approved test plan. Never edit, move, or delete existing
cards. If creation fails partway, report which cards were and weren't created and let the
user decide whether to retry (re-running is safe because of step 3).
