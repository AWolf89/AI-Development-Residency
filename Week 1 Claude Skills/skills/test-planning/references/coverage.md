# Coverage

Coverage is the share of code lines that ran during tests. It proves code ran, not that
it was checked, so it complements good assertions; it doesn't replace them.

Targets: critical paths 100 percent; overall at least 80 percent.

Commands (verify flags against current docs before first use):

```bash
# Python (pytest-cov: https://pytest-cov.readthedocs.io)
pip install pytest-cov
pytest --cov=<package> --cov-report=term-missing --cov-fail-under=80

# JavaScript (Vitest: https://vitest.dev/guide/coverage)
npx vitest run --coverage
```

For Vitest, set the 80 percent floor in the config's coverage thresholds so the run
fails below it. For critical paths, read the per-file report (`term-missing` shows
uncovered lines) and confirm each critical file is at 100 percent.

Never lower thresholds or add exclusions to make a run pass. If an exclusion is truly
needed (generated code, say), ask the user first and note it in the test plan.
