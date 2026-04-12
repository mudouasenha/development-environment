# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

## Workspace Orientation

This workspace root is the active shared development environment.

Environment governance is versioned in this Git repository at:

- `/mnt/c/Development`

Knowledge is versioned separately at:

- `/mnt/c/Development/knowledge`

Keep commit boundaries clean between:

- environment governance changes
- knowledge changes
- application or repo work

## Knowledge Graph Context

When possible, consult the Obsidian knowledge graph before implementing or documenting work:

- Vault root: `/mnt/c/Development/knowledge`
- Graph root: `/mnt/c/Development/knowledge/Knowledge Graph`

Use this graph as the source for durable architecture context, API contracts, product flows, and important project decisions.

Do not treat the graph as the source of truth for runtime state, secrets, generated artifacts, or operational environment wiring.

Use the hybrid workflow:

- ingest durable new sources placed under `/mnt/c/Development/knowledge/raw`
- file durable query results back into the graph when they should survive the current chat
- run periodic graph health checks with `/mnt/c/Development/system/ai/scripts/graph-lint.sh`

When a change affects architecture, contracts, product flows, or environment policy:

- update or link the corresponding knowledge note
- update `/mnt/c/Development/system/docs/environment` if the change affects operational environment truth

Code is the executable truth. Environment docs are the operational truth. The knowledge graph is the conceptual and historical truth.
