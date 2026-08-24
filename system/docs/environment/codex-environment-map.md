# Codex Environment Map

Date: 2026-04-11
Status: Active

## Summary

- Purpose: shared Codex environment with workspace-owned AI assets and user-owned runtime state
- Primary workspace root: `/mnt/c/Development`
- Primary runtime user home: `/home/matheus/.codex`
- Date established: `2026-04-11`
- Owner: `matheus`

## Design Goal

Separate user-scoped runtime state from workspace-scoped shared AI assets.

- User level owns identity, auth, session history, approvals, and local caches.
- Workspace level owns versioned skills, agents, plugins, registries, adapters, and environment documentation.

## User-Level Runtime

### Runtime Home

- Path: `/home/matheus/.codex`
- Purpose: live runtime state expected by Codex

### User-Scoped Assets

- Config: `/home/matheus/.codex/config.toml`
- Auth and credentials: `/home/matheus/.codex/auth.json`, `/home/matheus/.codex/.credentials.json`
- Sessions and history: `/home/matheus/.codex/sessions`, `/home/matheus/.codex/history.jsonl`
- Logs and state DBs: `/home/matheus/.codex/log`, `/home/matheus/.codex/logs_2.sqlite`, `/home/matheus/.codex/state_5.sqlite`
- Rules and approval memory: `/home/matheus/.codex/rules/default.rules`
- Plugin cache: `/home/matheus/.codex/plugins`
- Temp and cache dirs: `/home/matheus/.codex/tmp`, `/home/matheus/.codex/cache`

### Active Runtime Settings

- Default model: `gpt-5.4`
- Reasoning effort: `medium`
- Approval mode: `user`
- Enabled runtime features:
  - `codex_hooks = true`
  - `multi_agent = true`
  - `smart_approvals = true`
- Trusted projects:
  - `/mnt/c/Users/mathe/Documents/Development/source/repos`
  - `/mnt/c/Users/mathe/Documents/Development/source/repos/prova-ai-api`
  - `/mnt/c/Users/mathe/Documents/Development/source/repos/prova-ai-widget`
  - `/mnt/c/Users/mathe/Documents/Development/source/repos/next-ph`
  - `/mnt/c/Users/mathe/Documents/Development/source/repos/prova-ai/prova-ai-widget`
  - `/mnt/c/Users/mathe/Documents/Development/source/repos/prova-ai/prova-ai-api`
  - `/mnt/c/Users/mathe/Documents/Development/source/repos/portfolio`
  - `/mnt/c/Development`

### Hooks

- Event: `SessionStart`
- Command: `node /mnt/c/Development/system/ai/adapters/codex/session-start.js`
- Purpose: sync workspace-managed MCP server manifests into the user runtime config
- Observed hook surface also includes `PreToolUse` in local plugin docs
- No documented skill-level hook event observed for `SkillInvoked` or `SkillLoaded`

## Workspace-Level Shared Assets

### Workspace Root

- Path: `/mnt/c/Development`
- Purpose: shared environment root

### Canonical AI Asset Root

- Path: `/mnt/c/Development/system/ai`
- Purpose: versioned AI capability layer

### Shared Directories

- Tools workspaces: `/mnt/c/Development/tools`
- Adapters: `/mnt/c/Development/system/ai/adapters`
- Agents: `/mnt/c/Development/system/ai/agents`
- Plugins: `/mnt/c/Development/system/ai/plugins`
- Skills: `/mnt/c/Development/system/ai/skills`
- Registry: `/mnt/c/Development/system/ai/registry`
- MCP registry: `/mnt/c/Development/system/ai/registry/mcp`
- Imported sources: `/mnt/c/Development/system/ai/sources`
- Supporting docs: `/mnt/c/Development/system/docs/environment`

Current tool workspaces:

- `/mnt/c/Development/tools/career-ops`
- `/mnt/c/Development/tools/open-design`

### Installed Shared Capabilities

- Plugin bundles:
  - `superpowers`
  - `.NET plugin pack`
- Skill libraries:
  - `canonical workspace skills`
  - `promoted Codex system skills`
  - `imported-active infrastructure skills under source namespaces`

### Canonical Infra Tooling Layer

- Authored source of infra tooling wrappers: `/mnt/c/Development/repos/infra/skills`
- Bootstrap skill: `/mnt/c/Development/repos/infra/skills/infra-tooling-bootstrap`
- Wrapper skills:
  - `/mnt/c/Development/repos/infra/skills/tflint`
  - `/mnt/c/Development/repos/infra/skills/infracost`
  - `/mnt/c/Development/repos/infra/skills/gcp-recommender`
- Shared pinned version manifest:
  - `/mnt/c/Development/repos/infra/skills/infra-tooling-bootstrap/references/tool-versions.env`
- Shared bootstrap script:
  - `/mnt/c/Development/repos/infra/skills/infra-tooling-bootstrap/scripts/bootstrap-infra-tools.sh`

### Infra Tooling Policy

- CLI wrapper skills belong in the canonical skills repo.
- Tool versions are pinned in the manifest and validated before use.
- Downloaded binaries do not belong in the repository.
- User-local install locations such as `~/.local/bin` are preferred for pinned CLI tools.
- `gcloud` is treated as an externally managed dependency that is validated, not vendored.
- Runtime platform products such as OpenCost and Kubecost belong in infrastructure code and cluster operations, not in the workstation tool bootstrap path.

## Adapter / Mount Strategy

### Symlinks or Mounts

- `/home/matheus/.codex/agents` -> `/mnt/c/Development/system/ai/agents`
- `/home/matheus/.codex/skills` -> `/mnt/c/Development/system/ai/skills`
- `/home/matheus/.codex/superpowers` -> `/mnt/c/Development/system/ai/plugins/shared/superpowers`

### Preserved Local State

Keep these user-level paths local even after migration:

- `/home/matheus/.codex/config.toml`
- `/home/matheus/.codex/auth.json`
- `/home/matheus/.codex/.credentials.json`
- `/home/matheus/.codex/sessions`
- `/home/matheus/.codex/cache`
- `/home/matheus/.codex/log`
- `/home/matheus/.codex/tmp`
- `/home/matheus/.codex/plugins`

Managed MCP realizations are written into `/home/matheus/.codex/config.toml`, but the manifest source of truth lives under `/mnt/c/Development/system/ai/registry/mcp`.

## Shared Experiential Memory

Hindsight is the official environment-wide memory provider for experiential memory across supported coding agents.

- Provider: Hindsight self-hosted Docker deployment
- API: `http://localhost:8888`
- Persistent database: Docker named volume `hindsight-data`
- Hermes: `memory.provider: hindsight`, with the Hindsight plugin active
- Codex: user-scoped Hindsight MCP realization in `~/.codex/config.toml`
- Claude Code and OpenCode: user-scoped Hindsight coding-agent integrations
- Canonical operational reference: `/mnt/c/Development/system/docs/environment/hindsight-memory-integration.md`

Runtime credentials and integration files remain outside the versioned workspace. Hindsight stores experiential memory; the knowledge graph remains the source of curated conceptual and historical truth.

### Rationale

- Why Codex still needs the user runtime home: it stores identity, auth, sessions, approvals, runtime state, and plugin cache there
- Why shared assets should live in the workspace: they are reusable, versioned, and meant to be shared across projects and tools

## Plugin and MCP Integrations

### Enabled Plugins

- `notion@openai-curated`
  - Source: `/home/matheus/.codex/plugins/cache/openai-curated/notion/fb0a18376bcd9f2604047fbe7459ec5aed70c64b`
  - Status: `enabled`
  - Notes: active runtime plugin with imported source preserved under `/mnt/c/Development/system/ai/sources/imported-plugins/notion-openai-curated`

### Connected Tools

- Web access: `yes`
- Shell execution: `yes`
- Parallel tool execution: `yes`
- Sub-agents: `yes`
- MCP servers / apps:
  - `Notion`
  - Workspace-managed MCP registry synchronized into `~/.codex/config.toml`

## Workspace Instruction Layer

### Instruction Files

- Root instruction file: `/mnt/c/Development/AGENTS.md`
- Additional instruction files: repo-local `AGENTS.md` files where present

### Important Rules

- Shell wrapper requirement: `prefix all commands with rtk`
- Documentation source of truth: `/mnt/c/Development/knowledge` and `/mnt/c/Development/knowledge/Knowledge Graph`
- Editing constraints: keep runtime secrets out of the shared workspace and prefer shared AI assets under `/mnt/c/Development/system/ai`
- Infra tooling rule: keep CLI wrappers and version pins in `/mnt/c/Development/repos/infra/skills`, but keep installed binaries outside the repo

## Knowledge / Documentation Layer

### Canonical Knowledge Paths

- Vault root: `/mnt/c/Development/knowledge`
- Graph root: `/mnt/c/Development/knowledge/Knowledge Graph`
- Architecture notes: `/mnt/c/Development/knowledge/systems/Development Environment Target Architecture.md`
- Environment docs: `/mnt/c/Development/system/docs/environment`

### Drift Checks

- Older or stale documented path: `/mnt/c/Development/Development/Knowledge Graph`
- Replacement path: `/mnt/c/Development/knowledge/Knowledge Graph`
- Action taken: `updated /mnt/c/Development/AGENTS.md and environment docs`

## Verification Checklist

- Runtime home exists and is readable.
- Shared workspace asset root exists and is readable.
- All configured symlinks resolve correctly.
- The configured plugin list matches what Codex exposes at runtime.
- The root instruction file points to real paths.
- Knowledge graph paths exist.
- A new Codex session can see the expected skills, agents, and plugins.

## Current Environment Snapshot

```text
Environment name: Development shared Codex environment
Workspace root: /mnt/c/Development
Runtime home: /home/matheus/.codex
Default model: gpt-5.4
Enabled plugins: notion@openai-curated
Shared skills root: /mnt/c/Development/system/ai/skills
Shared agents root: /mnt/c/Development/system/ai/agents
Knowledge graph root: /mnt/c/Development/knowledge/Knowledge Graph
Root instruction file: /mnt/c/Development/AGENTS.md
Shared experiential memory: Hindsight at http://localhost:8888
Infra tooling manifest: /mnt/c/Development/repos/infra/skills/infra-tooling-bootstrap/references/tool-versions.env
Notes: runtime state remains in ~/.codex; shared AI assets are workspace-owned and mounted by symlink; infra CLI binaries are user-local and version-pinned by canonical wrapper skills
```
