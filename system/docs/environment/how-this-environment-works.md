# How This Environment Works

Date: 2026-04-11
Status: Active

## Overview

This environment is built around a single shared root:

- `/mnt/c/Development`

It separates:

- user-scoped runtime state
- workspace-scoped shared development assets
- long-term knowledge and documentation

The goal is to keep the development environment organized, reproducible, and usable across projects without pushing secrets or local runtime state into the shared workspace.

## Top-Level Structure

The main directories under `/mnt/c/Development` are:

- `README.md`
  - root entrypoint doc for the environment
- `development.code-workspace`
  - VS Code workspace file for opening the full environment
- `AGENTS.md`
  - root working instructions for Codex
- `repos/`
  - grouped project repositories
- `system/`
  - shared AI and environment infrastructure
- `knowledge/`
  - Obsidian vault and knowledge graph
- `archive/`
  - archived or backup material
- `inbox/`
  - temporary intake area

## Repository Layout

Repositories are grouped by primary operational category:

- `repos/product/`
  - active product families
- `repos/lab/`
  - experiments, learning projects, and exploratory work
- `repos/infra/`
  - tooling and shared infrastructure
- `repos/archive/`
  - old but still reachable repositories

Current grouped layout:

- `repos/product/prova-ai/prova-ai-api`
- `repos/product/prova-ai/prova-ai-ui`
- `repos/product/prova-ai/prova-ai-widget`
- `repos/lab/personal-projects/cachara`
- `repos/lab/personal-projects/portfolio`
- `repos/lab/ai-csharp-practice`
- `repos/lab/next-app`
- `repos/lab/next-ph`
- `repos/infra/skills`
- `repos/archive/booking-modular-monolith`
- `repos/archive/devops-directive-kubernetes-course`

These are copied working roots. The old source locations were not deleted.

## Shared AI Layer

Shared AI infrastructure lives under:

- `/mnt/c/Development/system/ai`

Main subdirectories:

- `skills/`
  - canonical shared skills
- `agents/`
  - shared agent definitions
- `plugins/shared/`
  - shared plugin bundles
- `sources/`
  - imported sources, caches, and references
- `registry/`
  - provenance records
- `adapters/`
  - tool-specific runtime integration notes
- `scripts/`
  - maintenance scripts

This is the shared capability layer for the environment.

## Canonical vs Imported

The environment uses a strict distinction:

- canonical
  - the maintained shared source of truth
- imported
  - mirrored, cached, or upstream material kept separate from canonical
- runtime-only
  - local state that stays in user home

Current canonical decisions:

- `/mnt/c/Development/system/ai/skills` is the canonical shared skills root
- it was initially populated from `.agents/skills/skills`
- `/mnt/c/Development/repos/infra/skills` is now the authored and versioned canonical skills repository
- `/mnt/c/Development/system/ai/skills` should point to that repo as the deployed runtime path
- imported-active skill packs may live under labeled namespaces inside that repo, such as `imported/anthropic/*` and `imported/dotnet/*`
- infrastructure CLI wrapper skills also live in that repo, including:
  - `infra-tooling-bootstrap`
  - `tflint`
  - `infracost`
  - `gcp-recommender`
- selected user-level skills were promoted:
  - `~/.codex/skills/.system/*`
  - `~/.codex/skills/gsd-*`

Current canonical infrastructure tooling decisions:

- pinned infra tool versions live in `/mnt/c/Development/repos/infra/skills/infra-tooling-bootstrap/references/tool-versions.env`
- the shared bootstrap workflow lives in `/mnt/c/Development/repos/infra/skills/infra-tooling-bootstrap/scripts/bootstrap-infra-tools.sh`
- `tflint` and `infracost` are installed into a user-local bin directory, not committed into the repo
- `gcloud` is validated by canonical skills but remains an externally managed dependency
- runtime platform services such as OpenCost and Kubecost are managed through infrastructure code and cluster operations, not the workstation bootstrap path

Current imported sources are tracked in:

- `/mnt/c/Development/system/ai/sources/imported-skills/SOURCES.md`

Key sources include Anthropic, dotnet, Codex User Skills, HashiCorp, and Anton Babenko.

Imported-active rule:

- if an imported skill pack should be visible to Codex without full promotion, place it under `repos/infra/skills/imported/<source>/...`
- keep the source namespace and provenance intact
- do not flatten imported skills into the top-level canonical namespace unless they are explicitly promoted

The governing rule is simple:

- canonical assets live in one place only
- imported assets do not become canonical unless explicitly promoted

See:

- `/mnt/c/Development/system/docs/environment/canonical-promotion-policy.md`

## Codex Runtime Model

Codex still uses:

- `~/.codex`

as its live runtime home.

That user-home runtime still owns:

- `config.toml`
- auth and credential files
- sessions
- cache
- logs
- temp state
- plugin cache
- approval memory

But the shared assets are mounted from the workspace by symlink:

- `~/.codex/agents` -> `/mnt/c/Development/system/ai/agents`
- `~/.codex/skills` -> `/mnt/c/Development/system/ai/skills`
- `~/.codex/superpowers` -> `/mnt/c/Development/system/ai/plugins/shared/superpowers`

This gives you:

- personal runtime state
- shared reusable capability
- one centralized environment root

## Shared MCP Workflow

Workspace-managed MCP servers follow the same ownership split:

- manifest source of truth: `/mnt/c/Development/system/ai/registry/mcp/*.json`
- runtime realization: `~/.codex/config.toml`

The adapter scripts live in:

- `/mnt/c/Development/system/ai/adapters/codex`

The main sync entrypoint is:

- `/mnt/c/Development/system/ai/adapters/codex/sync-mcp-servers.js`

The session bootstrap hook is:

- `/mnt/c/Development/system/ai/adapters/codex/session-start.js`

The sync writes a managed block into `config.toml` and leaves unmanaged MCP entries alone. This keeps shared MCP definitions versioned in the workspace without collapsing all user runtime state into the shared tree.

## Knowledge Layer

Knowledge lives under:

- vault root: `/mnt/c/Development/knowledge`
- graph root: `/mnt/c/Development/knowledge/Knowledge Graph`

Use this structure:

- `knowledge/raw`
  - immutable source material for ingest
- `knowledge/Knowledge Graph`
  - synthesized durable notes
- `knowledge/logs`
  - append-only ingest, query, and lint logs
- `knowledge/outputs`
  - optional generated reports and artifacts

Use this layer for:

- architecture context
- product flows
- contracts
- migration notes
- long-term system memory

This is a documentation and knowledge system, not the live runtime source of truth.

## Versioning

Two environment-level areas are now versioned separately:

- `/mnt/c/Development/knowledge`
  - separate Git repo for knowledge content, logs, raw sources, and shared Obsidian vault configuration
- `/mnt/c/Development`
  - separate Git repo for environment governance files and `system/docs/environment`

This keeps durable knowledge and environment governance backed up without forcing the entire `/mnt/c/Development` tree into one repository.

Do not version:

- `~/.codex`
- runtime secrets
- session state
- imported caches or disposable tool state unless there is an explicit retention reason

The `/mnt/c/Development` environment repo should include:

- `AGENTS.md`
- `README.md`
- `REMOTE-SETUP.md`
- `development.code-workspace`
- `system/docs/environment/**`

## Knowledge Workflows

The knowledge graph follows a hybrid workflow:

- ingest
  - new durable source material is added under `knowledge/raw`, then summarized and linked into the graph
- query
  - durable syntheses from useful investigations are filed back into the graph
- lint
  - periodic health checks look for orphan notes, weak links, stale synthesis, and structural gaps

Use these helpers:

- `system/ai/scripts/graph-lint.sh`
- `system/ai/scripts/check-doc-sync.sh`

Use these supporting files:

- `system/docs/environment/hybrid-knowledge-workflow.md`
- `Knowledge Graph/index.md`
- `logs/ingest-log.md`
- `logs/query-log.md`
- `logs/lint-log.md`

## Daily Workflow

Recommended use:

1. Open `/mnt/c/Development/development.code-workspace`.
2. Read `/mnt/c/Development/AGENTS.md` if you need the current root instructions.
3. Work from repos under `/mnt/c/Development/repos`.
4. Use the knowledge graph when architecture or flow context matters.
5. Keep commits in `knowledge` and `system/docs/environment` scoped to their own truth domains.
6. Keep environment-level changes inside `/mnt/c/Development/system`.

## Maintenance Workflow

Maintenance scripts live in:

- `/mnt/c/Development/system/ai/scripts`

Main scripts:

- `verify-links.sh`
  - checks that critical roots exist and Codex symlinks still resolve correctly
- `graph-lint.sh`
  - runs a lightweight health check over graph structure and link hygiene
- `check-doc-sync.sh`
  - reminds you when changed paths likely require environment docs or knowledge graph updates
- `sync-imports.sh`
  - refreshes imported sources and re-promotes approved Codex skills into canonical
- `restore-backups.sh --apply all`
  - restores the original pre-migration Codex directories from the dated backups

Recommended maintenance habits:

- after environment-level changes:
  - run `verify-links.sh`
  - run `check-doc-sync.sh <changed-paths...>`
- periodically for knowledge hygiene:
  - run `graph-lint.sh`
- when imported sources change:
  - run `sync-imports.sh`
- when rollback is needed:
  - use `restore-backups.sh --apply ...`

## Documentation Sync Rule

When a change affects:

- architecture
- API or behavioral contracts
- product or user flows
- environment policy
- AI runtime or canonical/imported boundaries

update the relevant documentation before treating the work as complete.

Use this split:

- update `system/docs/environment` for operational environment truth
- update the knowledge graph for durable architecture, contract, flow, or decision knowledge

If the change is environment-level and architecture-relevant, update both.

## Operational Boundaries

Do:

- keep canonical shared assets in `system/ai`
- keep imported assets in `system/ai/sources`
- keep runtime secrets and session state in `~/.codex`
- use registry records and docs when promoting assets

Do not:

- treat plugin cache as canonical
- merge full user overlays into canonical by default
- move secrets into `/mnt/c/Development`
- let tool-specific layouts redefine the canonical structure

## Important Docs

Use these as the main references:

- Root entrypoint:
  - `/mnt/c/Development/README.md`
- Environment map:
  - `/mnt/c/Development/system/docs/environment/codex-environment-map.md`
- Design rationale:
  - `/mnt/c/Development/system/docs/environment/environment-design-rationale.md`
- Canonical promotion policy:
  - `/mnt/c/Development/system/docs/environment/canonical-promotion-policy.md`
- Codex adapter:
  - `/mnt/c/Development/system/ai/adapters/codex/README.md`

## Current State

The environment is already usable and validated for Codex.

What is complete:

- shared AI layer
- Codex cutover
- grouped repo copies
- knowledge path alignment
- maintenance scripts
- policy and environment docs

What remains optional:

- Claude Code cutover
- Cursor cutover
- making the copied repos the only active roots in the future
- further maintenance automation if real usage reveals gaps
