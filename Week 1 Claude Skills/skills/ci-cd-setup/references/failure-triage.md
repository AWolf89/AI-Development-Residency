# Explaining CI failures

Read only the failed step's log (`gh run view <id> --log-failed`). Explain: which check,
what it means in plain language, the likely cause, the proposed fix. Then ask.

| Failed step | Usually means | Typical fix |
|---|---|---|
| Install | Missing/incompatible package, stale lockfile | Fix requirements or regenerate lockfile |
| Lint | Code breaks a rule (unused import, likely bug) | Fix the code; don't disable rules without asking |
| Format check | Code not formatted | Run the formatter locally, commit |
| Tests | A test fails | Reproduce locally; fix code or test via test-planning |
| Coverage | Below 80 percent | Add tests via test-planning |
| Dependency scan | A package has a known vulnerability | Upgrade to a fixed version; if none, replace the package |
| Passes locally, fails in CI | Environment difference (versions, missing env var, OS) | Compare versions; check the var is set as a GitHub secret |

Analogy: the CI log is the inspector's report - read the first failure; later ones are
often knock-on effects.
