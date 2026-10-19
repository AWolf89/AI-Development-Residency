# Choosing a test framework

Present the options, recommend one, and let the user decide. Verify current status on the
official sites before recommending; tools change.

## Python
- **pytest** (https://docs.pytest.org) - the widely used standard; plain `assert`
  statements, powerful fixtures (reusable setup). Usually the recommendation.
- **unittest** (built into Python) - no install needed, but more boilerplate.

## JavaScript / TypeScript
- **Vitest** (https://vitest.dev) - fast, modern, Jest-compatible API; best fit for Vite
  projects and new projects.
- **Jest** (https://jestjs.io) - long-established, huge ecosystem; common in older or
  React Native projects.

## End-to-end (browser)
- **Playwright** (https://playwright.dev) - multiple browsers, auto-waiting, strong tooling.
- **Cypress** (https://www.cypress.io) - friendly interactive runner; historically more
  limited across browsers.

Analogy: the framework is the referee - it runs the match (your tests) and announces
the score (pass/fail). The choice matters less than using one consistently.
