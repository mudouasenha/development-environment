# Hindsight Shared Memory Integration

Date: 2026-08-24
Status: Active

## Decision

Hindsight is the official shared experiential-memory provider for the `/mnt/c/Development` environment. It is scoped to the supported agents used under this environment, including:

- Hermes
- Codex
- Claude Code
- OpenCode

The provider is self-hosted through Docker Compose and is intentionally separate from the tracked documentation and knowledge repositories.

## Runtime Service

- Setup: `/mnt/c/Development/tools/hindsight_memory_kit/hindsight-setup`
- API: `http://localhost:8888`
- Control Plane: `http://127.0.0.1:9999`
- Database: Docker named volume `hindsight-data`
- Container policy: Compose `restart: unless-stopped`
- Backups: host directory `Hindsight Backups` as configured by the Compose setup

The Docker Compose `.env` file, API keys, Codex authentication, database volume, and backup contents are runtime state. They must remain outside the tracked environment and knowledge repositories.

## Agent Wiring

The live user-scoped integrations are:

| Agent | Runtime surface | Role |
|---|---|---|
| Hermes | Hermes profile memory configuration with `provider: hindsight`; Hindsight plugin active | Native memory provider and memory tools |
| Codex | `~/.codex/config.toml` Hindsight MCP entry | MCP access to Hindsight coding-agent memory |
| Claude Code | `~/.claude/settings.json` Hindsight lifecycle hooks | Session and prompt lifecycle integration |
| OpenCode | `~/.config/opencode/opencode.json` Hindsight plugin | Coding-agent integration |
| Cursor | `~/.cursor/hooks.json` Hindsight lifecycle hooks | Coding-agent integration |
| Copilot | `~/.copilot/hooks/hindsight-coding-agents.json` | Coding-agent integration |

These files are user-scoped runtime realizations and are not workspace configuration sources of truth. The shared environment documents the policy and boundaries; the agent installers own their runtime wiring.

## Authority Boundaries

Use Hindsight for experiential memory:

- user and environment preferences
- lessons learned from completed work
- workflow outcomes and troubleshooting history
- reusable observations that improve future agent work

Keep other truth domains in their existing authorities:

- code and tests: executable truth
- `system/docs/environment`: operational environment truth
- `/mnt/c/Development/knowledge/Knowledge Graph`: curated conceptual and historical truth
- `knowledge/raw`: immutable source material for later synthesis

Do not use Hindsight as a replacement for architecture notes, API contracts, live configuration, or source code. Do not store secrets, credentials, authentication codes, or raw private configuration in Hindsight or the knowledge graph.

## Verification

Hermes provider status:

```bash
hermes memory status
```

Expected provider state:

```text
Provider:  hindsight
Plugin:    installed
Status:    available
```

Hindsight service health, from the devbox shell:

```bash
cd /mnt/c/Development/tools/hindsight_memory_kit/hindsight-setup
docker compose --env-file .env -f docker-compose.yml ps
curl -fsS http://127.0.0.1:8888/health
```

## Operations

- Start or recreate the service with `docker compose ... up -d --remove-orphans`.
- Leave `restart: unless-stopped` enabled so Docker restarts the service after the Docker engine starts.
- Create and verify backups before upgrades.
- Do not run `docker compose down -v` casually; it can remove Hindsight data and authentication volumes.
- Keep agent runtime credentials and generated integration files in user home.
- When changing the provider or integration model, update this document and the related knowledge note together.

## Related Documents

- `/mnt/c/Development/AGENTS.md`
- `/mnt/c/Development/system/docs/environment/how-this-environment-works.md`
- `/mnt/c/Development/system/docs/environment/codex-environment-map.md`
- `/mnt/c/Development/knowledge/systems/Development Environment Target Architecture.md`
- `/mnt/c/Development/knowledge/systems/Hermes Agent Workspace Integration.md`
- `[[Hindsight Shared Memory Provider]]`
