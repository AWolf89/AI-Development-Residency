# Docker and secrets

Goal: `docker-compose.yml` is safe to commit because it contains names, never values.

Safe:
```yaml
services:
  app:
    environment:
      - API_KEY        # name only: value comes from the shell environment
```
Start it through the manager so the shell has the values:
`<manager> run -- docker compose up`

Unsafe (never):
```yaml
    environment:
      - API_KEY=sk-live-abc123   # value written in the file
```

Also never bake secrets into images (no `ENV API_KEY=...` or copying `.env` in a
Dockerfile): anyone with the image can read them.

Verify the exact injection command in the chosen manager's docs before first use.
