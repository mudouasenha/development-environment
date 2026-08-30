# OpenDesign Container Agent Runtime

Status: Active

## Purpose

OpenDesign runs from `/mnt/c/Development/tools/open-design` in Docker Desktop. The container uses the host Codex installation as its generation runtime without storing credentials in tracked files or image layers.

## Local Boundary

```text
browser on 127.0.0.1:7456
  -> OpenDesign daemon container (uid 1001)
  -> read-only host Codex binary
  -> Docker volume open-design_codex_home
```

The one-shot `codex-auth-init` service reads the host's Codex `auth.json`, `config.toml`, and agent-role definitions through read-only WSL mounts. It copies them into `open-design_codex_home`, applies mode `0600` to login/config files, and exits before OpenDesign starts. The volume and running container are credential-bearing trusted local state.

The daemon remains bound to `127.0.0.1`. `OD_API_TOKEN` protects browser/API access independently from Codex authentication.

## Local Files

- Base Compose: `/mnt/c/Development/tools/open-design/deploy/docker-compose.yml`
- Codex overlay: `/mnt/c/Development/tools/open-design/deploy/docker-compose.codex.yml`
- Secret-bearing daemon env: `deploy/.env` (ignored)
- Non-secret local path overrides: `deploy/.env.codex.local` (ignored)
- Full runbook: `/mnt/c/Development/tools/open-design/docs/deployment/docker.md`

## Startup

From `/mnt/c/Development/tools/open-design`:

```bash
docker compose \
  --env-file deploy/.env \
  --env-file deploy/.env.codex.local \
  -f deploy/docker-compose.yml \
  -f deploy/docker-compose.codex.yml \
  up -d --no-build
```

In a WSL shell without Docker CLI integration, invoke Docker Desktop's Windows CLI at:

```text
/mnt/c/Program Files/Docker/Docker/resources/bin/docker.exe
```

Use the same Compose arguments. Docker Desktop must be running.

## Verification

```bash
docker compose \
  --env-file deploy/.env \
  --env-file deploy/.env.codex.local \
  -f deploy/docker-compose.yml \
  -f deploy/docker-compose.codex.yml \
  ps -a

docker exec open-design codex login status
docker exec open-design node -e \
  "fetch('http://127.0.0.1:7456/api/agents').then(r=>r.json()).then(x=>console.log(x.agents.find(a=>a.id==='codex')))"
```

Expected state:

- `codex-auth-init` exited with code 0
- `open-design` is healthy
- Codex reports `available: true`, `authStatus: "ok"`, and a live model catalog
- container memory limit is at least 1 GiB; 384 MiB caused exit-137 restart loops during agent detection

## Security Rules

- Never place tokens in Compose YAML, `.env.codex.local`, commands, logs, or images.
- Keep the daemon loopback-bound.
- Treat `open-design_codex_home` as sensitive and do not export or attach it.
- Authenticate Codex on the host, then rerun Compose to refresh the private volume.
- Use `OD_CODEX_SANDBOX=danger-full-access` only for a trusted single-user deployment after a real sandbox failure.
- Do not mount a host Hermes Python virtualenv. A Hermes container lane requires a separately maintained private runtime image and runtime authentication.
