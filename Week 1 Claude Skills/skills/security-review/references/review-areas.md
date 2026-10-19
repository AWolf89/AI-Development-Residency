# Review areas

Walk each area that applies. Explain each finding: risk, how an attacker could use it
(conceptually), an analogy, and the fix.

## OWASP Top 10
Based on the OWASP Top 10 (https://owasp.org/www-project-top-ten/). The categories below
follow the 2021 edition; a newer edition may exist - check the site and update this file.
- A01 Broken access control - can a user reach data or actions that aren't theirs?
- A02 Cryptographic failures - passwords hashed (bcrypt/argon2)? HTTPS? sensitive data encrypted?
- A03 Injection - SQL, shell, or HTML built from user input? (includes XSS)
- A04 Insecure design - missing limits, trust in the client, no abuse cases considered
- A05 Security misconfiguration - debug mode on, default passwords, open admin panels, permissive CORS
- A06 Vulnerable and outdated components - see Dependencies
- A07 Identification and authentication failures - weak passwords allowed, no lockout, session handling
- A08 Software and data integrity failures - unverified updates, unsafe deserialisation
- A09 Security logging and monitoring failures - are attacks and failures logged (without secrets)?
- A10 Server-side request forgery (SSRF) - does the server fetch URLs a user supplies?

## APIs
- Every endpoint checks authentication and that the caller owns the object (not just "logged in").
- Input validated (types, lengths, allowed values); unexpected fields rejected.
- Rate limiting on login, signup, and expensive endpoints.
- Responses don't leak internal fields, stack traces, or other users' data.
- CORS allows only intended origins.

## Docker
- Container runs as a non-root user.
- Base image is official, pinned, and recent.
- No secrets in images or Dockerfiles.
- Only needed ports exposed; databases not published to the public internet.

## n8n workflows
- Webhooks that trigger workflows require authentication (header auth or similar).
- Credentials use n8n's credential store or the secret manager, never values in nodes.
- Code nodes and HTTP nodes don't run or fetch user-supplied input unchecked.
- The n8n editor isn't publicly reachable without authentication.

## Dependencies
- Run scripts/dep_audit.sh; review each finding's severity and whether a fixed version exists.
- Unmaintained or abandoned packages flagged.
- Lockfiles committed (package-lock.json, poetry.lock / pinned requirements).
