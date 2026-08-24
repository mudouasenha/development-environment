# Development Environment Entrypoint

Date: 2026-04-11
Status: Active

## Start Here

- VS Code workspace: `/mnt/c/Development/development.code-workspace`
- Root instructions: `/mnt/c/Development/AGENTS.md`
- Shared environment root: `/mnt/c/Development/system/ai`
- Knowledge graph: `/mnt/c/Development/knowledge/Knowledge Graph`

## Core Environment Docs

- Environment map:
  - `/mnt/c/Development/system/docs/environment/codex-environment-map.md`
- Shared memory integration:
  - `/mnt/c/Development/system/docs/environment/hindsight-memory-integration.md`
- Design rationale:
  - `/mnt/c/Development/system/docs/environment/environment-design-rationale.md`
- Canonical promotion policy:
  - `/mnt/c/Development/system/docs/environment/canonical-promotion-policy.md`
- Knowledge graph operating model:
  - `/mnt/c/Development/system/docs/environment/knowledge-graph-operating-model.md`
- Hybrid knowledge workflow:
  - `/mnt/c/Development/system/docs/environment/hybrid-knowledge-workflow.md`

## Versioned Repos

- Knowledge repo:
  - `/mnt/c/Development/knowledge`
- Environment governance repo:
  - `/mnt/c/Development`
- Remote setup note:
  - `/mnt/c/Development/REMOTE-SETUP.md`

## Maintenance Scripts

- Scripts root:
  - `/mnt/c/Development/system/ai/scripts`
- Verify live links:
  - `/mnt/c/Development/system/ai/scripts/verify-links.sh`
- Lint the knowledge graph:
  - `/mnt/c/Development/system/ai/scripts/graph-lint.sh`
- Refresh imported sources:
  - `/mnt/c/Development/system/ai/scripts/sync-imports.sh`
- Restore pre-migration backups:
  - `/mnt/c/Development/system/ai/scripts/restore-backups.sh --apply all`

## Shared AI Roots

- Canonical skills:
  - `/mnt/c/Development/system/ai/skills`
- Shared agents:
  - `/mnt/c/Development/system/ai/agents`
- Shared plugins:
  - `/mnt/c/Development/system/ai/plugins/shared`
- Imported sources:
  - `/mnt/c/Development/system/ai/sources`
- Registry metadata:
  - `/mnt/c/Development/system/ai/registry`

Canonical skills are authored in the nested Git repository:

- `/mnt/c/Development/repos/infra/skills`

When skill files change, stage and commit them in that repository, not in `/mnt/c/Development`.

## Repository Groups

- Product:
  - `/mnt/c/Development/repos/product`
- Lab:
  - `/mnt/c/Development/repos/lab`
- Infra:
  - `/mnt/c/Development/repos/infra`
- Archive:
  - `/mnt/c/Development/repos/archive`

### Current Product Family

- ProvaAI:
  - `/mnt/c/Development/repos/product/prova-ai/prova-ai-api`
  - `/mnt/c/Development/repos/product/prova-ai/prova-ai-ui`
  - `/mnt/c/Development/repos/product/prova-ai/prova-ai-widget`

## Runtime Boundary

Keep these as user-scoped runtime state:

- `~/.codex/config.toml`
- `~/.codex/auth.json`
- `~/.codex/.credentials.json`
- `~/.codex/sessions`
- `~/.codex/cache`
- `~/.codex/log`
- `~/.codex/tmp`

Shared assets are mounted into Codex through these symlinks:

- `~/.codex/agents` -> `/mnt/c/Development/system/ai/agents`
- `~/.codex/skills` -> `/mnt/c/Development/system/ai/skills`
- `~/.codex/superpowers` -> `/mnt/c/Development/system/ai/plugins/shared/superpowers`

## Recommended Workflow

1. Open `/mnt/c/Development/development.code-workspace`.
2. Read `/mnt/c/Development/AGENTS.md`.
3. Work from repos under `/mnt/c/Development/repos`.
4. Use the knowledge graph when architecture or flow context matters.
5. Ingest durable new sources into `knowledge/raw` and file valuable syntheses back into the graph.
6. Run `graph-lint.sh` periodically and `verify-links.sh` after environment-level changes.
