# Boundary cases

The clear cases do not need a reference. These are the ones where "stay in scope" and "do the
job properly" appear to conflict.

The default across all of them: **do the minimum that makes the requested change correct and
safe, and report the rest.**

---

## A bug blocks your change

You cannot implement the requirement without fixing it.

Fix the minimum needed to unblock, state it explicitly in the summary as an in-scope-by-
necessity change, and explain why it was unavoidable. Do not fix the general case of the bug,
and do not fix its siblings elsewhere in the file.

If the fix is large, risky, or touches shared code, stop and ask instead. The user may want it
in a separate change with its own review.

## A bug does not block your change

Observation. Do not touch it, however small, however certain you are.

This is the most common creep path, because the fix is usually one line and feels free. It is
not free: it widens the diff, it is unreviewed against its own requirements, and it may be
load-bearing in a way you cannot see from here.

## Your change orphans existing code

A function becomes unreachable, an import unused, a branch dead.

Leave it, note it. Exception: a linter or build step that fails on unused imports makes
removal necessary — do it and say so.

## Tests

- **Write tests for the change you made.** This is in scope by default; a change without
  coverage is incomplete, not minimal. If the project has no test suite, ask rather than
  introducing one.
- **A test was already failing before you started.** Observation. Note it in the summary and
  make clear it predates your change, so nobody attributes it to you.
- **Your change breaks an existing test.** In scope to investigate. If the test encoded
  behavior you were asked to change, update it and say so. If it caught a real break in your
  work, fix your work. If it is unclear which, ask — silently updating a test to pass is one
  of the most damaging things you can do.

## The formatter rewrites the whole file

An editor or hook reformats on save, producing hundreds of unrelated lines.

Revert the unrelated hunks and keep only your change. If you cannot, say so plainly and ask
how they want to handle it. A diff where the real change is invisible among whitespace cannot
be reviewed properly.

## The code around you is poor

Bad names, deep nesting, duplication, no types.

Work within it. Match the existing style even where you would never write it that way. A file
in one consistent bad style is more maintainable than one split between two styles.

If it is bad enough to be worth fixing, that is an observation, and a valuable one — but it is
a separate piece of work with its own review.

## You need a helper that does not exist

Write the smallest one that serves your change, local to where it is used. Do not build a
general utility, do not add it to a shared module, and do not refactor existing code to use
it. Generalizing is a design decision that belongs to whoever owns that module.

## A dependency is outdated or vulnerable

Never upgrade unilaterally — version changes affect everything, and the blast radius is
invisible from inside one ticket.

A known vulnerability is worth raising immediately rather than filing as a routine
observation, but raising it is still the action, not upgrading.

## Config, environment, CI, and infrastructure files

Out of scope unless named explicitly. This includes lockfiles, CI pipelines, Dockerfiles,
linter configs, and environment settings. Changes here are nearly always broader in effect
than they look.

## Documentation

Update docs that your change makes wrong — a docstring on a function you altered, a README
line describing behavior you changed. That is part of making the change correct.

Do not write documentation that was missing before you arrived.

## Secrets, credentials, and destructive operations

If the work appears to require committing a credential, deleting data, or running something
irreversible, stop and ask regardless of scope. These are never implied by a change request.

---

## A shorter test

When unsure, ask: *if the reviewer saw this line in the diff, would they wonder why it is
there?* If yes, it is either out of scope or it needs an explanation in the summary. Both are
better than it appearing unannounced.
