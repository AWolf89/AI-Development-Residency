# n8n and the secret manager

Unverified - check https://docs.n8n.io before setting up, because features and plan
limits change:
- n8n has an "External Secrets" feature that connects to secret managers; it may be
  limited to paid or enterprise plans.
- The fallback is injecting secrets as environment variables when the n8n container
  starts (through the manager's run command), then referencing them in n8n. n8n may
  block environment-variable access in nodes by default via a setting.

Steps:
1. Check the user's n8n version and plan, and read the current docs for both methods.
2. Present what is available to them, with trade-offs, and let them choose.
3. Never paste secret values into workflow JSON; exported workflows get shared.
4. n8n's own encryption key (which protects its credential store) is itself a secret:
   it goes in the manager, never in a committed file.
