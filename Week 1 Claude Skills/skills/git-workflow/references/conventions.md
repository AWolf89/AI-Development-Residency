# Conventions

Spec: https://www.conventionalcommits.org

## Types (for both branches and commits)
| Type | Use for |
|---|---|
| feat | A new feature |
| fix | A bug fix |
| docs | Documentation only |
| test | Adding or fixing tests |
| refactor | Restructuring without changing behaviour |
| chore | Tooling, config, dependencies |
| ci | CI pipeline changes |
| perf | Performance improvements |
| style | Formatting only |
| build | Build system changes |

## Branch names
`type/short-description` - lowercase, words joined with hyphens, at most 50 characters.
Example: `feat/password-reset`, `fix/empty-email-signup`.

## Commit messages
`type(optional-scope): description`
- description: lowercase start, imperative ("add", not "added"), no trailing period,
  first line at most 72 characters.
- Breaking change: add `!` after the type (`feat!: drop v1 API`) and explain in the body.
- Optional body after a blank line: why the change was made.

Analogy: labels on moving boxes - anyone (or a script) knows what's inside without
opening them. This is what lets release tools build changelogs automatically later.
