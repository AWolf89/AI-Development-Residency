# Adding a deploy workflow (after the user picks a host)

1. Read the host's official GitHub Actions deploy docs; don't rely on memory.
2. Create `.github/workflows/deploy.yml` triggered only by `workflow_dispatch` (the
   manual "Run workflow" button) - never on push.
3. Pin every action to a SHA; set `permissions: contents: read` plus only what the host
   requires (comment why).
4. Deploy credentials come from GitHub secrets, set up via secrets-management.
5. Run CI's checks first in the same workflow (or require the commit to have passed CI)
   so a failing build can't be deployed.
6. Run check_workflow.py and go through a PR.
7. First deploy: walk the user through pressing "Run workflow" and checking the result.
