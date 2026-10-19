# Auditing a repo for leaked secrets (TruffleHog)

Docs: https://github.com/trufflesecurity/trufflehog - verify flags before first use.

1. Audit only the repos the user named this time.
2. Tell the user once: verification sends found keys to their provider to test whether
   they still work.
3. Scan full history of a local clone:
   `trufflehog git file://<path-to-repo>`
   (verification is on by default as of writing; confirm in the docs).
4. Also scan the working tree for uncommitted files:
   `trufflehog filesystem <path-to-repo>`
5. Report as a table: file, commit, detector, verified (live / not live / unknown).
   Never print full secret values; show at most the first 4 characters.
6. Any live or unknown finding -> leak response. Not-live findings still get rotated
   if unsure, and noted.
7. Re-running an audit is safe (read-only).
