# Storage standard (secret manager, manager-neutral)

One central store feeds every stage, so rotating a secret is one update.

| Stage | How secrets arrive |
|---|---|
| Local dev | The manager's CLI injects them: `<manager> run -- <command>` |
| Docker | Started through the manager CLI so variables reach containers (see docker.md) |
| n8n | See n8n.md (verify the current method first) |
| CI (GitHub Actions) | Manager's GitHub integration or action, or synced into GitHub secrets |
| Deploy (PaaS) | Manager's integration with the PaaS, or synced into its env settings |

Rules:
- The manager's access token goes in the OS keychain (macOS Keychain, Windows Credential
  Manager, Linux secret service) via the CLI's login command.
- Use one project per app and separate environments (dev, staging, prod). Never use
  prod secrets in dev or tests.
- A local `.env` is a fallback only, always gitignored, and only if the user chooses it.

Analogy: the manager is a key-cutting service that updates every copy of a key at once,
instead of visiting every place a spare is hidden.
