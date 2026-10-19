# Branch protection for main

The user changes GitHub settings; Claude only guides. GitHub's settings UI changes over
time, so check the current docs first:
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository

Goal settings for `main` (names may differ in the current UI - rulesets or branch
protection rules):
- Require a pull request before merging.
- Block force pushes.
- Block deletion.
- Later, once ci-cd-setup exists: require status checks (tests) to pass.

Note for a solo developer: requiring an approving review from someone else would block
you from merging your own PRs. Leave required approvals at 0 unless a teammate joins.

After the user saves the setting, test it: try `git push origin main` from a throwaway
change - it should be rejected. Then discard the throwaway change.
