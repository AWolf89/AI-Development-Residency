# Requiring CI before merging

The user changes the setting; Claude guides. Check GitHub's current docs, since the UI
changes: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository

1. Make sure the CI workflow has run at least once (the check name must exist).
2. In the repo's settings, open the protection rule or ruleset for `main` (created by
   git-workflow).
3. Enable "require status checks to pass before merging" and select the CI job
   (named `ci` in the templates).
4. Optionally require branches to be up to date before merging.
5. Test: open a PR with a deliberately failing test - the merge button should be
   blocked. Close the PR afterwards.

Solo developer: keep required approvals at 0, or you can't merge your own PRs.
