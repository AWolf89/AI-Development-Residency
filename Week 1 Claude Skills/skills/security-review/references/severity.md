# Severity ratings

Judge two things: how easy it is to exploit, and how bad the damage would be. Public
users means "only reachable after login" still counts as reachable.

| Severity | Meaning | Examples |
|---|---|---|
| Critical | Easy to exploit, severe damage (data breach, takeover) | SQL injection on a public form; no auth on an admin API |
| High | Serious damage, or easy to exploit with real damage | Users can read other users' data by changing an ID; outdated package with a known remote exploit |
| Medium | Real but limited damage, or harder to exploit | No rate limiting on login; verbose error messages leaking internals |
| Low | Minor, defence-in-depth | Missing security header; overly broad CORS on a read-only public endpoint |

Rule: when unsure between two levels, pick the higher.
Only Low findings that don't change behaviour, in this task's code, may be auto-fixed.
