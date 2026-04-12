# Environment Design Rationale

Date: 2026-04-11
Status: Active

## Purpose

Capture the main design decisions behind the `/mnt/c/Development` environment so the setup can be understood without chat history.

## Decision 1: Split Truth Domains

The environment uses separate truth domains:

- code = executable truth
- `system/docs/environment` = operational truth
- knowledge graph = conceptual and historical truth

Why:

- code should remain the authority on implementation behavior
- environment docs should remain the authority on tooling, adapters, scripts, and policies
- the knowledge graph should preserve durable understanding without becoming a duplicate config store

This reduces confusion and prevents the graph from drifting into runtime instructions or implementation duplication.

## Decision 2: Keep The Knowledge Graph Curated

The graph is intentionally agent-maintained but curated, not fully automatic.

Why:

- fully automatic note creation tends to produce noisy, low-value documentation
- graph updates often require judgment about what is durable versus disposable
- a curated graph stays smaller, more reliable, and more reusable across sessions

This is why the environment uses:

- ingest workflows
- durable query filing
- graph lint reminders

but does not force automatic note generation for every change.

## Decision 3: Keep Environment Docs Outside The Graph

Operational environment docs live under:

- `/mnt/c/Development/system/docs/environment`

instead of inside the knowledge graph.

Why:

- these docs govern the environment itself
- they belong next to the infrastructure they describe
- they change with tooling and runtime operations more directly than conceptual notes do

The graph can link to these docs, but it should not replace them.

## Decision 4: Centralize Shared AI Assets In The Workspace

Shared AI assets live under:

- `/mnt/c/Development/system/ai`

Why:

- skills, agents, shared plugins, adapters, and registries should be workspace-owned and reusable across projects
- this creates one canonical shared capability layer
- it avoids fragmented copies spread across repos and user home

This makes the AI layer easier to document, maintain, and evolve.

## Decision 5: Keep Codex Runtime State User-Scoped

Codex still uses `~/.codex` for:

- config
- auth
- sessions
- logs
- local cache
- approvals memory

Why:

- runtime identity and local state are personal
- secrets and transient state should not move into the shared workspace
- this preserves the normal Codex runtime model while still allowing a shared capability layer

The result is a hybrid:

- user home owns runtime state
- `/mnt/c/Development/system/ai` owns shared AI capability

## Decision 6: Add Karpathy-Style Knowledge Workflows Without Making The Wiki Absolute

The environment borrows from the LLM wiki pattern by adding:

- `knowledge/raw`
- ingest workflows
- durable query filing
- lint workflows
- index and log files

Why:

- this helps knowledge compound over time
- it gives the agent a persistent synthesis layer
- it improves cross-repo memory

But the wiki is not treated as the single source of truth for everything.

Why not:

- software environments need stronger operational boundaries than a pure wiki-first model
- code and environment behavior need clearer authorities

## Result

The current design aims to balance:

- strong operational boundaries
- reusable shared AI capability
- durable accumulated knowledge
- low risk of documentation pollution
- compatibility with real day-to-day development work

## When To Revisit This Design

Revisit the design if any of these start happening:

- the graph becomes noisy or stale
- environment docs and graph notes repeatedly contradict each other
- workspace-owned AI assets become fragmented again
- user-home runtime state starts leaking into the workspace
- the current ingest/query/lint workflow feels too manual for real use
