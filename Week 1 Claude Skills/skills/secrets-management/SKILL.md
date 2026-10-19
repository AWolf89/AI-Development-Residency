---
name: secrets-management
description: Keeps API keys, passwords, tokens, and other secrets out of code and Git by setting up a secret manager for local, Docker, n8n, CI, and deploys, installing a gitleaks pre-commit hook on every repo, auditing chosen repos with TruffleHog, and guiding rotation when a leak is found. Use when a project needs a secret or credential, when setting up a new repo, when the user mentions API keys, passwords, tokens, .env, environment variables, credentials, Doppler, 1Password, Infisical, gitleaks, or TruffleHog, asks to audit or scan a repo for secrets, or a secret may have leaked. Also use whenever Claude is about to write code that needs a credential. Do NOT use for user login or authentication design, encryption of app data, general security audits (use security-review), or storing personal passwords unrelated to software projects.
license: MIT
compatibility: Works in Claude Code, Claude.ai, and the API. Setup and audits need a terminal with git; the user must install the chosen secret manager CLI, gitleaks, and TruffleHog.
metadata:
  author: AWolf89
  owner: AWolf89
  version: 0.1.0
  category: security
  tags:
  - secrets
  - credentials
  - gitleaks
  - trufflehog
  - secret-manager
---

# Secrets Management

A secret is anything that grants access: API keys, passwords, tokens, database URLs with
passwords in them. Git remembers every version of every file, so a secret committed once
stays readable in history even after it is deleted. The defence is layered: keep secrets
in a secret manager, block them at commit time, audit for old leaks, and rotate fast.

## Critical rules

1. **Never write a secret value into code, config, docs, chat, or a commit.** Code reads
   secrets from environment variables; values come from the secret manager.
2. **Never ask the user to paste a secret into the chat.** Give them the command or
   dashboard step to store it themselves.
3. **A found leak means rotate first.** Stop other work, report it, and guide the user
   through rotation before anything else (`references/leak-response.md`).
4. **Rewriting Git history and force-pushing are destructive** and always need the
   user's explicit confirmation, every time.
5. **Claude never logs in to the user's accounts** (secret manager, GitHub, providers).
   The user performs rotations and dashboard changes; Claude guides step by step.
6. **The secret manager's own access token lives in the OS keychain**, never in a repo
   or a .env file that could be committed.

## Pick the mode

| Situation | Mode |
|---|---|
| New repo, or repo without the standard setup | A. Project setup |
| Writing code that needs a credential | B. Everyday coding |
| User asks to audit or scan | C. Audit |
| A secret is found or suspected leaked | D. Leak response |

First time each mode is used: explain each piece in plain language with an analogy
(the user is learning). Later runs: just do the work and report.

## A. Project setup

1. Run `python3 scripts/check_repo_hygiene.py <repo>` and show the result.
2. Secret manager: the user has not chosen one yet. If none is configured, read
   `references/manager-options.md`, present the options, and let the user choose. Until
   then, follow `references/storage-standard.md` in its manager-neutral form.
3. `.gitignore`: ensure it ignores `.env` and `.env.*` (but not `.env.example`).
4. `.env.example`: only if the project needs secrets - names with fake values.
5. Docker: `references/docker.md` - secrets injected at run time, never inline in
   `docker-compose.yml`.
6. n8n (if used): `references/n8n.md` - verify the current approach in n8n's docs first.
7. CI and deploys: `references/ci-deploy.md`.
8. Pre-commit hook: `bash scripts/install_hook.sh <repo>` (gitleaks). It refuses to
   overwrite an existing hook; if one exists, show it and ask how to combine them.
9. Re-run the hygiene check; all items should pass.
10. Suggest security-review. Don't start it without the user.

## B. Everyday coding

- Read secrets from environment variables (`os.environ["API_KEY"]` in Python,
  `process.env.API_KEY` in JavaScript). Fail with a clear error naming the missing
  variable, never its value.
- Add the variable name to `.env.example` and tell the user which secret to add to the
  manager and how.
- Never put real-looking secrets in tests; use obvious fakes (`test-not-a-real-key`).

## C. Audit

Follow `references/audit.md`. Audit only the repos the user names this time. TruffleHog
runs with verification on, which tests found keys against their providers - mention
that once per audit. Present findings as a table: file, commit, detector, verified
(live / not live / unknown). Any finding -> Mode D. Then suggest security-review.

## D. Leak response

Follow `references/leak-response.md`: stop, report, guide rotation, confirm the old
secret is dead, then ask about history cleanup (destructive - explicit confirmation).

## Examples

**New repo.** User: "Set up my new FastAPI repo."
Actions: hygiene check (fails: no .gitignore entry, no hook); no manager chosen ->
present options, user picks later -> manager-neutral setup; add .gitignore entries;
install hook; re-check passes; suggest security-review.

**Code needs a key.** Writing an OpenAI call.
Actions: read `OPENAI_API_KEY` from the environment; add the name to `.env.example`;
tell the user to store the key in their secret manager with the exact command.

**Audit finds a live key.** TruffleHog: verified AWS key in commit a1b2c3.
Actions: stop; report; guide the user to deactivate and replace it in the AWS console;
update the manager; confirm the old key fails; ask whether to clean history.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Hook blocks a commit with a fake test value | Pattern match on a fake | Use an obvious fake, or add a narrow allow rule to `.gitleaks.toml` after asking |
| `gitleaks: command not found` | Not installed | Give install steps from the official README; never skip the hook silently |
| install_hook.sh refuses | Existing pre-commit hook | Show it; ask whether to chain gitleaks into it |
| TruffleHog reports "unknown" | Provider couldn't be checked | Treat as live until the user rotates it |
| App can't find a variable | Not injected | Check the app is started through the manager's run command |
| Secret pasted in chat by the user | Accident | Tell them to rotate it; don't repeat the value |

## Where this skill stops

It handles where secrets live and whether they leaked. Broader vulnerabilities belong
to security-review; commit and push practices to git-workflow.
