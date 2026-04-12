# Codex Environment Map Template

Use this template to document a Codex setup in a new machine, repo, or shared workspace.

## Summary

- Purpose: `[what this environment is for]`
- Primary workspace root: `[absolute path]`
- Primary runtime user home: `[absolute path]`
- Date established: `[YYYY-MM-DD]`
- Owner: `[name or team]`

## Design Goal

Separate user-scoped runtime state from workspace-scoped shared AI assets.

- User level should own identity, auth, session history, approvals, and local caches.
- Workspace level should own versioned skills, agents, plugins, registries, and environment documentation.

## User-Level Runtime

Document the runtime home used by Codex.

### Runtime Home

- Path: `[example: /home/you/.codex]`
- Purpose: live runtime state expected by Codex

### User-Scoped Assets

- Config: `[config.toml path]`
- Auth and credentials: `[auth.json path]`, `[credentials path]`
- Sessions and history: `[sessions path]`, `[history path]`
- Logs and state DBs: `[logs path]`, `[state DB path]`
- Rules and approval memory: `[rules path]`
- Plugin cache: `[plugins cache path]`
- Temp and cache dirs: `[tmp path]`, `[cache path]`

### Active Runtime Settings

- Default model: `[model]`
- Reasoning effort: `[level]`
- Approval mode: `[mode]`
- Enabled runtime features:
  - `[feature]`
  - `[feature]`
- Trusted projects:
  - `[absolute path]`
  - `[absolute path]`

### Hooks

- Event: `[event name]`
- Command: `[command]`
- Purpose: `[what this hook does]`

## Workspace-Level Shared Assets

Document the canonical shared layer checked into the workspace.

### Workspace Root

- Path: `[example: /mnt/c/Development]`
- Purpose: shared environment root

### Canonical AI Asset Root

- Path: `[example: /mnt/c/Development/system/ai]`
- Purpose: versioned AI capability layer

### Shared Directories

- Adapters: `[path]`
- Agents: `[path]`
- Plugins: `[path]`
- Skills: `[path]`
- Registry: `[path]`
- Imported sources: `[path]`
- Supporting docs: `[path]`

### Installed Shared Capabilities

- Agent packs:
  - `[pack or agent group]`
- Plugin bundles:
  - `[plugin]`
- Skill libraries:
  - `[library or source]`

## Adapter / Mount Strategy

Document how user runtime paths point at workspace-owned assets.

### Symlinks or Mounts

- `[runtime path]` -> `[workspace path]`
- `[runtime path]` -> `[workspace path]`
- `[runtime path]` -> `[workspace path]`

### Preserved Local State

Keep these user-level paths local even after migration:

- `[path]`
- `[path]`
- `[path]`

### Rationale

- Why Codex still needs the user runtime home: `[reason]`
- Why shared assets should live in the workspace: `[reason]`

## Plugin and MCP Integrations

Document which integrations are actually enabled, not just installed on disk.

### Enabled Plugins

- `[plugin name]`
  - Source: `[workspace bundle path or plugin cache path]`
  - Status: `[enabled/disabled]`
  - Notes: `[why it exists]`

### Connected Tools

- Web access: `[yes/no]`
- Shell execution: `[yes/no]`
- Parallel tool execution: `[yes/no]`
- Sub-agents: `[yes/no]`
- MCP servers / apps:
  - `[name]`
  - `[name]`

## Workspace Instruction Layer

Record any repo-level behavior modifiers.

### Instruction Files

- Root instruction file: `[path]`
- Additional instruction files: `[path or none]`

### Important Rules

- Shell wrapper requirement: `[example: prefix all commands with rtk]`
- Documentation source of truth: `[knowledge path or docs path]`
- Editing constraints: `[summary]`

## Knowledge / Documentation Layer

### Canonical Knowledge Paths

- Vault root: `[path]`
- Graph root: `[path]`
- Architecture notes: `[path]`
- Environment docs: `[path]`

### Drift Checks

- Older or stale documented path: `[path]`
- Replacement path: `[path]`
- Action taken: `[updated instruction file / left note / TODO]`

## Verification Checklist

Use these checks after setup or migration.

- Runtime home exists and is readable.
- Shared workspace asset root exists and is readable.
- All configured symlinks resolve correctly.
- The configured plugin list matches what Codex exposes at runtime.
- The root instruction file points to real paths.
- Knowledge graph paths exist.
- A new Codex session can see the expected skills, agents, and plugins.

## Current Environment Snapshot

Fill this section with the real values for the environment you are documenting.

```text
Environment name:
Workspace root:
Runtime home:
Default model:
Enabled plugins:
Shared skills root:
Shared agents root:
Knowledge graph root:
Root instruction file:
Notes:
```
