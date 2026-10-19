# CI and deploy secrets

- GitHub Actions: use the manager's official GitHub integration or action, or sync
  secrets into repository secrets. Reference them as `${{ secrets.NAME }}`; never echo
  them in logs.
- PaaS: use the manager's integration with the host, or sync into the host's
  environment-variable settings.
- Use separate environments: CI gets test secrets, production gets prod secrets.
- The user performs dashboard and integration setup; Claude provides exact steps from
  the official docs of the chosen manager and host.
