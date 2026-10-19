# External services in tests

Rule 1 always applies: never production data or real accounts.

| Option | How | Trade-off |
|---|---|---|
| Mock | Replace the service with a fake that returns canned answers | Fast, offline, safe; can miss real API changes |
| Test copy | A throwaway real instance (e.g. Postgres in Docker, a separate test Notion database) | Catches real mismatches; slower, needs setup |
| Mixed (common) | Mock in unit tests, test copies in integration tests | Speed where it helps, realism where it matters |

Analogy: a mock is rehearsing with someone reading the other actor's lines; a test copy
is a dress rehearsal with the real cast and no audience.

Record the per-service choice under "Project choices" in the test plan.
