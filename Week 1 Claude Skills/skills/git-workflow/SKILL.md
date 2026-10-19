---
name: git-workflow
description: Runs the user's Git and GitHub workflow - feature branches named type/short-description, one Conventional Commit per feature, pushes to feature branches, pull requests with a standard description, merge commits, conflict help, and branch protection setup - while explaining each new Git command in plain language. Use whenever code is ready to commit, when the user says commit, push, branch, pull request, PR, merge, conflict, rebase, git, or GitHub, after self-review passes, or when starting work in a repo. Never commits to main. Do NOT use for general GitHub Actions or CI setup (use ci-cd-setup), for code review of a PR's contents, or for secrets found in history (use secrets-management).
license: MIT
compatibility: Works in Claude Code with git and the GitHub CLI (gh). In Claude.ai or the API without a terminal, Claude gives the exact commands for the user to run.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.1.0
  category: engineering
  tags:
  - git
  - github
  - pull-requests
  - conventional-commits
---

# Git Workflow

Git is a save-point system for code: commits are save points, branches are parallel
copies for experiments, and pull requests are the review step before changes join
`main`. The user is learning Git (comfort 2/5), so commands are explained as they go.

## Critical rules

1. **Never commit or push to `main`.** All work happens on a branch and arrives through
   a PR. If the current branch is `main`, create a branch first.
2. **Ask before:** opening a PR, merging a PR, resolving a merge conflict, and deleting
   any branch. Ask separately each time.
3. **Force-push only with explicit confirmation**, every time, after explaining what it
   will overwrite. Never force-push `main`.
4. **Pushing to feature branches is allowed without asking.**
5. **Explain every new command** before running it (what it does, why, an analogy if it
   helps). Mention familiar commands again occasionally, about once per session.
6. **Never move or edit Kanban cards.** PRs only link to them.

## Step 1: Start work on a branch

Run `bash scripts/preflight.sh` before the first change. It reports the current branch,
uncommitted changes, and whether you are on `main`. Then create the branch:

```bash
git switch main && git pull
git switch -c feat/password-reset
```

Branch name: `type/short-description` (types and rules in
`references/conventions.md`). Check it with
`python3 scripts/check_names.py branch <name>`.

## Step 2: Commit - one per feature

When the feature is done and self-review has passed, commit once with a Conventional
Commit message:

```bash
git add <files>
git commit -m "feat(auth): add password reset"
```

Check the message first with `python3 scripts/check_names.py commit "<message>"`.
Stage only the files for this feature; never `git add .` blindly - review `git status`
first so stray files (like .env) aren't included. If an extra fix is needed before the
PR is opened, use `git commit --amend` so the feature stays one commit (explain amend
the first time). After a branch is pushed, amending requires a force-push, so prefer a
second commit then and mention why.

## Step 3: Push

```bash
git push -u origin <branch>
```

## Step 4: Open the PR (ask first)

Ask: "Open a PR from <branch> into main?" On yes, fill `assets/pr-template.md`
(summary, why, changes, how tested, self-review table, linked Kanban card) and run:

```bash
gh pr create --base main --head <branch> --title "<commit message>" --body-file <filled template>
```

Link the Kanban card's URL in the PR body. Do not move or edit the card.

## Step 5: Merge (ask first)

Ask: "Merge PR #N into main with a merge commit?" On yes:

```bash
gh pr merge <N> --merge
```

Then switch back and update: `git switch main && git pull`.

## Step 6: Clean up and hand off

Ask before deleting the merged branch (local and remote, separately named). Then, if the
repo has no `.github/workflows/` folder, suggest the ci-cd-setup skill.

## Merge conflicts

When Git reports a conflict: show the conflicting section, explain in plain language
what each side changed and why Git can't choose (two people edited the same sentence),
propose a resolution, and ask before applying it. Details:
`references/conflicts.md`.

## Branch protection (one-time per repo)

If `main` isn't protected, guide the user through GitHub's settings to require PRs
before merging (the user changes the setting; Claude never does). Steps:
`references/branch-protection.md`.

## Examples

**Feature.** After self-review passes on password reset.
Actions: preflight (on `feat/password-reset`, clean); `git status`; add the feature's
files; commit `feat(auth): add password reset`; push; ask to open PR; on yes, create it
with the template and Kanban link; later, ask to merge; merge commit; ask about deleting
the branch; no CI folder -> suggest ci-cd-setup.

**On main by mistake.** Preflight shows `main` with uncommitted changes.
Actions: explain; `git switch -c fix/<name>` (the changes come along); continue.

**User asks to force-push.** Explain it overwrites the remote branch's history and what
would be lost; proceed only on explicit confirmation; refuse for `main`.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Push rejected (non-fast-forward) | Remote branch has commits you don't | `git pull --rebase` on the feature branch after explaining; never force-push to "fix" it without asking |
| `gh: command not found` / not logged in | GitHub CLI missing | Give install link https://cli.github.com and have the user run `gh auth login` themselves |
| Push to main blocked by GitHub | Branch protection working | Move work to a branch |
| Committed .env by mistake | Staged too much | Don't push; hand to secrets-management |
| Commit message check fails | Not Conventional Commits | Rewrite per `references/conventions.md` |
| No terminal (Claude.ai) | Surface limitation | Give the commands with explanations for the user to run |

## Where this skill stops

It handles branches, commits, PRs, merges, and conflicts. CI pipelines belong to
ci-cd-setup; code quality to self-review-checklist; leaked secrets to secrets-management.
