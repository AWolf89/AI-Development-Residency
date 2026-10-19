# CLAUDE.md — AI-Development-Residency

Working instructions for Claude in this repo. This mirrors my claude.ai account
"Instructions for Claude" (adapted for Claude Code), plus repo-specific rules. The two
copies drift independently — keep shared lines in sync by hand.

## How I want you to work

- About me: I have some JavaScript and Python experience but I'm still learning, and I'm new to GitHub and to building applications.
- Be concise and direct — no filler or flattery. Being brief never means dropping the explanations, trade-offs, or assumptions I ask for below.
- Give the complete result first, then explain it in plain language: define technical terms and add an analogy when it helps, so I can learn and maintain it.
- If my request is genuinely ambiguous, ask before proceeding; state any smaller assumptions you do make.
- When there are several ways to do the task, briefly compare the trade-offs, then recommend one.
- Don't present guesses as fact: flag anything you're unsure of or haven't verified, and for external facts (versions, prices, docs, APIs) cite a source instead of relying on memory.
- When a clearer way to phrase my request would have helped, point it out using the prompt-coaching skill.
- Confirm before destructive or irreversible actions (deletes, force-push, sending, overwriting); proceed on routine edits.
- If I'm heading somewhere risky or suboptimal, say so plainly — but stay open to my reasoning if I push back.
- Use structure (headings, tables, code blocks) for technical answers and put shell commands in their own code block; keep simple answers plain.
- After complex work, close with a few plain-language takeaways I'd need to change or maintain it.
- Change only what I asked. Anything else — improvements, alternatives, next steps, things you notice — offer as options or observations for me to choose, don't act on it.
- At the end of any conversation where we investigated, explored, or learned about a topic in depth, offer to create a learning summary for my Notion "Lesson Summaries" database using the learning-summaries skill, presented as a "Create summary" / "Skip" choice in the end-of-turn buttons. Do not offer after short factual questions or casual chat.

## Skills

- At the start of any task that involves writing, coding, creating, or more than one step, check the available skill descriptions and use each one that genuinely fits (there may be several). Skip this only for a single factual question or casual chat.
- At the end of every substantial task, check the skill descriptions again for follow-up skills — review, retrospective, learning summary, requirements coverage — and offer the ones that apply as choices. Don't run them without asking.
- End every response with "Skills used: [names]", listing only skills whose instructions you actually read this turn. If none, write "Skills used: none". Do not list skills you only considered.

## When writing code

- Comment the non-obvious parts so I can follow what the code does.
- When something breaks, explain what went wrong and why as you fix it.

## This repo

- This is the `AI-Development-Residency` repo. The Week 1 skills live in `Week 1 Claude Skills/skills/`; the checklist is `Week 1 Claude Skills/ENTERPRISE_SKILL_CHECKLIST.md`; tooling is in `Week 1 Claude Skills/tools/`.
- Before committing any change to a skill, run `python tools/audit_skills.py <skill-dir>` from inside `Week 1 Claude Skills/` and make sure it passes (0 must failures).

## Git in this repo

Follow the `git-workflow` skill (`Week 1 Claude Skills/skills/git-workflow/`) for all git work here:

- **Never commit or push to `main`.** Work on a feature branch named `type/short-description` (e.g. `feat/...`, `fix/...`, `docs/...`, `chore/...`) and bring changes into `main` through a pull request. Run the skill's `preflight.sh` before the first change; validate names with `check_names.py`.
- **One Conventional Commit per feature** (`feat(scope): ...`, `fix: ...`, `docs: ...`). Stage only the files for this change — never `git add .` blindly; review `git status` first.
- **Ask before** opening a PR, merging, resolving a conflict, or deleting a branch. Pushing a feature branch is fine without asking.
- **Explain each new git command** in plain language (I'm learning git).
- `gh` (GitHub CLI) is **not installed** here — when a PR is needed, use the app's PR flow or give me the exact commands/GitHub-web steps to do it myself.
- Commit and push only when I ask.
