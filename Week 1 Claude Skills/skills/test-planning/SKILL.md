---
name: test-planning
description: Plans tests together with the user before code is written, then builds features test-first (TDD) - asking questions to shape the plan, proposing critical paths, explaining each test as it is written, and enforcing 100 percent coverage on approved critical paths with an 80 percent overall floor. Use after a design or plan is approved, when the user asks to build, add, or fix something that needs tests, says "plan tests", "write tests", "TDD", "test this", "coverage", or reports a bug to fix. Bug fixes always get a failing regression test first. Do NOT use for tiny non-bug changes (renames, typos, formatting), for explaining testing concepts with nothing being built, for reviewing finished code, or for setting up CI pipelines.
license: MIT
compatibility: Works in Claude Code, Claude.ai, and the API. Running tests needs code execution; creating Kanban cards needs a connected Notion tool.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.1.0
  category: engineering
  tags:
  - testing
  - tdd
  - coverage
  - quality
---

# Test Planning

Tests written after the code tend to test what the code does, not what it should do.
This skill plans tests with the user first, then builds test-first. The user is learning
testing, so every test is explained as it is written.

## Critical rules

1. **Tests never touch production data or real accounts.** No production databases, live
   API keys, or real user accounts in any test, ever. If a test would need one, stop and
   ask how to provide a test copy or mock.
2. **Bug fixes always start with a failing regression test**, whatever the task size. The
   test must fail for the right reason before the fix is written.
3. **Only an explicit "approved" counts as sign-off** on a test plan. Anything else is
   feedback: ask "Reply 'approved' to start, or tell me what to change."
4. **Test-first.** No feature code before its failing test exists.

## Step 1: Choose what applies

| Task | Tests |
|---|---|
| Tiny, not a bug (rename, typo) | None - this skill stops here |
| Any bug fix | Regression test first (go to Step 6) |
| Medium | Unit + integration |
| New app | Unit + integration + end-to-end (E2E) |

Use the size from design-review if one was set; otherwise state the size and let the
user override.

## Step 2: Settle per-project choices (first time per project)

If the project has no test setup yet, explain the options and let the user choose:
- **Framework** - read `references/frameworks.md` and present the trade-offs for the
  project's language. Recommend one, but the user decides.
- **External services** (APIs, databases, Notion) - read `references/external-services.md`
  and present mock vs. test-copy options. The user decides; Rule 1 always applies.

Record both choices in the test plan so later sessions don't re-ask.

## Step 3: Plan together by asking

Interview the user in small batches (3 questions at a time) rather than presenting a
finished plan. Cover: what the feature must do, what inputs are valid and invalid, what
should happen on errors and empty data, and what would hurt users most if it broke.

Then propose the **critical paths** - code that must never break, such as login and
access control, payments, data writes and deletes, and security checks. The user
approves or edits the list. Critical paths need 100 percent coverage.

## Step 4: Write the plan and get "approved"

Write `docs/test-plan/<kebab-case-feature>.md` from `references/test-plan-template.md`,
keeping its headings exactly. Then run:

```bash
python3 scripts/check_test_plan.py docs/test-plan/<name>.md
```

Exit code 0 means it is complete. Present the plan ending with: *"Reply 'approved' to
approve the plan and create the test cards listed above, or tell me what to change."*

## Step 5: After "approved" - build test-first

1. Create the plan's listed cards in Notion (`references/notion-kanban.md`).
2. For each behaviour: write one failing test in `tests/`, run it, and show it failing.
   Explain the test in plain language: what it checks, why it matters, and an analogy
   for any new concept. Then write the minimum code to pass, and run it again.
3. When all tests pass, run coverage (`references/coverage.md`). Critical paths must be
   100 percent and the overall total at least 80 percent. If below, write the missing
   tests - never lower the threshold or exclude files to pass.
4. If the plan needs to change mid-build, stop, explain why, update the plan, and get a
   new "approved".

## Step 6: Bug fixes

1. Write a test that reproduces the bug in `tests/`. Run it and confirm it fails because
   of the bug, not a typo in the test.
2. Explain what the test checks and why it stops the bug coming back.
3. Fix the code, then run the full suite so nothing else broke.
4. For a tiny bug, no plan file is needed; state the test in chat.

## Step 7: Hand off

Report results (tests passing, coverage numbers), then suggest the self-review-checklist
skill. Do not start it without the user.

## Examples

**New feature.** After design-review approval of a URL shortener.
Actions: ask about valid URLs, duplicates, and errors; propose critical paths (creating
links, redirect lookups, input validation); write `docs/test-plan/url-shortener.md` with
unit, integration, and E2E sections and cards; run the checker; wait for "approved";
create cards; write each failing test with an explanation, then code; check coverage;
suggest self-review.

**Bug.** User: "The signup form accepts empty emails."
Actions: write `tests/test_signup.py::test_rejects_empty_email`, run it, show it failing,
explain it, fix the validation, run the full suite.

**Tiny non-bug.** User: "Rename the config variable." Actions: no tests; this skill stops.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| New test passes immediately | It doesn't test the new behaviour, or the behaviour already exists | Check the assertion; make sure it fails first |
| Coverage below threshold | Untested branches | Write tests for the reported lines; never lower thresholds |
| Test needs a real account or key | No test copy exists | Stop (Rule 1); ask the user to set up a mock or test copy |
| Flaky test (passes sometimes) | Timing, randomness, or shared state | Fix the cause; don't retry until it passes |
| No code execution (Claude.ai chat) | Surface limitation | Write tests and code, and give the exact commands for the user to run |
| Notion unavailable | Not connected | Show the card list for manual entry; continue only if the user says so |

## Where this skill stops

It plans, writes, and runs tests and the code that passes them. It does not review code
(self-review-checklist does) or set up CI (ci-cd-setup does).
