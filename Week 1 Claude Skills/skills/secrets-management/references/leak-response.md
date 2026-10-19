# Leak response

Order matters: kill the secret first, clean up second.

1. **Stop** other work. Tell the user which secret, where (file, commit), and whether it
   is live. Do not repeat the value.
2. **Rotate (user does it, Claude guides):** in the provider's dashboard, create a new
   secret, then revoke or delete the leaked one. Give exact steps from the provider's
   official docs.
3. **Update** the secret manager with the new value (user runs the command Claude gives).
4. **Confirm** the app works with the new secret and the old one is rejected.
5. **Check** the provider's usage or audit logs for activity you don't recognise.
6. **Ask about history cleanup.** Explain: rewriting history (e.g. git filter-repo)
   removes the secret from old commits but changes every later commit ID, and requires
   a force-push that can break other clones. It is destructive and optional once the
   secret is rotated. Proceed only on the user's explicit confirmation, and confirm
   again before the force-push.
7. Note the incident (what leaked, when, how fixed) for the user's records.

Analogy: lost keys - change the locks first, then search for where you dropped them.
