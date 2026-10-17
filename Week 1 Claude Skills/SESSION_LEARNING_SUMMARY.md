# Session Learning Summary

A plain-language recap of everything we covered, written so you can come back to it later.
Date: 2026-10-15

---

## 1. What makes an enterprise-grade skill

A **skill** is a folder with a `SKILL.md` file (instructions + a YAML header called *frontmatter*)
plus optional bundled files (scripts, references, templates). Claude always reads the skill's
**description**, but only reads the full body when the skill is triggered. That "load it only
when needed" idea is called **progressive disclosure**, and it drives most of the best practices.

The six things that separate an enterprise skill from a hobby one:

| Area | The point |
|---|---|
| **Triggering (description)** | The description decides *when* the skill fires. Write it around words users actually type, with "Use when…" triggers and "Do NOT use for…" exclusions. This is where most skills fail. |
| **Progressive disclosure** | Keep `SKILL.md` lean (the decision layer); push deep detail into `references/` files loaded on demand. |
| **Determinism** | Anything with one correct method → a bundled **script**, not prose. Scripts are reliable; instructions are re-guessed each time. |
| **Governance** | Version it, review it like code, least-privilege tools, no hardcoded secrets, confirm side-effecting actions. |
| **Evals** | Test prompts that *should* and *should not* trigger it. Track triggering accuracy separately from output quality. |
| **Design principles** | Idempotent (safe to re-run), safe-by-default, consistent output, graceful failure. |

> You have this as a full checklist in `ENTERPRISE_SKILL_CHECKLIST.md`.

---

## 2. Git vs GitHub (the big one for you)

These sound alike but are different things:

- **git** = a tool *on your computer* that tracks your files' history. Works offline.
- **GitHub** = a *website* that stores copies of git projects online, for backup and sharing.

Key terms, in plain language:

| Term | What it means | Analogy |
|---|---|---|
| **Repository (repo)** | The project folder git is watching | The whole filing cabinet |
| **Commit** | A saved snapshot with a message | A labeled checkpoint you can return to |
| **Staging (`git add`)** | Choosing which changes go in the next commit | Putting items in a box before sealing it |
| **Branch (`main`)** | A line of history | The main timeline of your project |
| **Remote (`origin`)** | A named link to a hosted copy (GitHub) | The address of your cloud backup |
| **Push / Pull** | Upload commits / download commits | Syncing your saves to/from the cloud |

**Mental model:** git is the save system, commits are your save points, GitHub is the cloud
backup you *push* your saves to.

**Important caveat from this session:** your commits are saved locally, but I could **not verify**
they're actually on GitHub — the check failed because git has no stored login here. To confirm,
look at [github.com/AWolf89/Claude-Skills](https://github.com/AWolf89/Claude-Skills) and check
whether commit `6da3b30` is there.

---

## 3. How skills actually trigger

- **Available ≠ used.** A skill being installed doesn't mean it fires. It only takes effect when
  it's **invoked** (its instructions get loaded).
- **Chat vs Code behave differently:**
  - In **claude.ai chat**, enabled skills can **auto-fire** by matching your message to their
    description.
  - In **Claude Code**, skills are available but *I* have to recognize the fit and invoke them —
    there's no automatic matching engine.
- **There is no "trigger engine" you build.** It's built into the products. The dial *you* control
  is the **description**, verified with the **eval suites**.
- **For guaranteed firing**, don't rely on matching:
  - **Slash command** (`/skill-name`) — runs it every time, on demand.
  - **Hook** — a rule that fires automatically on an event (see §5).

---

## 4. Slash commands and chaining skills

- A standard slash command invokes **one** skill. There's no built-in "run several at once."
- But you can author a **custom slash command** (a markdown file in `.claude/commands/`) whose
  body tells me to run several skills **in sequence** — a pipeline.
- **Skills compose best sequentially, not simultaneously.** Loading many at once makes them
  compete and dilute each other. One governs a phase, then hands off to the next.

---

## 5. Keeping standards "on" while building

"Invoke once" (a slash command) is *not* reliable always-on enforcement. For standards that stay
on, use two different tools:

| Tool | What it is | Best for |
|---|---|---|
| **`CLAUDE.md`** | A file at your repo root, loaded into *every* turn automatically while working in that repo | Judgment-based guidance (your preferences, standards) |
| **Hooks** | Rules that fire automatically on events (e.g., after each edit, before a commit) and run a command | Deterministic gates — can actually *block* bad changes |

Your skills already ship scripts that make ideal hooks (e.g. `check_scope.py`, `check_coverage.py`,
`validate_requirements.py`, and repo-level `tools/audit_skills.py`).

**Division of labor:** deterministic checks → hooks; judgment habits → `CLAUDE.md`; manual
"do this workflow now" → slash command.

---

## 6. "Instructions for Claude" (account preferences)

- It's a **claude.ai account field** for durable, cross-conversation preferences about *how* you
  want me to work.
- **Put here:** always-relevant, personal, concise directives. **Keep out:** project-specific
  rules (those go in `CLAUDE.md`), secrets, and long documents.
- **Two limits:**
  1. **Character cap (hard):** your field accepted ~1,563 characters, so the rumored ~1,500 cap
     doesn't apply to your account. Watch the field's counter to find the real limit.
  2. **Instruction-following reliability (soft, more important):** these are *guidance that
     influences* me, not *code that executes*. The more rules you add, the less reliably each one
     is followed. ~10–18 crisp, always-relevant lines is a healthy range.
- **Critical caveat:** this field governs **chat**, **not** Code. I confirmed it isn't loaded in
  this Code session. To have the same preferences here, mirror them into a `CLAUDE.md`.
- **The filter for any line:** "Is this true in almost every conversation?" Yes → account field.
  Project- or tool-specific → `CLAUDE.md`. Must-happen-every-time → a hook.

Your finished 12-line instruction set is live in your account field (cross-checked for overlap,
clear, and concise).

---

## 7. Moving a Code conversation to Chat

- I'm **not aware of a built-in "move to chat"** feature, and couldn't confirm one exists.
- Workarounds: **export the transcript** to a file, or have me **write a handoff summary** to
  paste into a new chat. Both copy the content; neither keeps the session live in both places.

---

## What's in your repo now

```
Claude Skills/
├── ENTERPRISE_SKILL_CHECKLIST.md
├── SESSION_LEARNING_SUMMARY.md   (this file)
├── skills/        6 skills, all passing the audit
│   ├── concept-checkpoints/        (updated to 0.2.0)
│   ├── prompt-coaching/            (updated to 0.2.0)
│   ├── requirements-elicitation/
│   ├── requirements-traceability/
│   ├── retrospectives/
│   └── scope-discipline/
└── tools/         audit_skills.py, collisions.py
```

Git history (local): 8 commits. GitHub sync is **unconfirmed** — verify on the website.

---

## Suggested next steps (your choice — not done yet)

- Create a `CLAUDE.md` so your preferences apply in Code (mirror the 12 lines + 2 coding lines).
- Verify the repo is actually on GitHub; set up git login here if we need to push.
- Add a top-level `README.md` indexing the six skills.
- Wire `audit_skills.py` as a pre-commit hook so standards are enforced automatically.
