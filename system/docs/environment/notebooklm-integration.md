# NotebookLM Integration

Date: 2026-04-15
Status: Active

## Purpose

Define how NotebookLM is integrated into the `/mnt/c/Development` environment as an operational capability.

This document is the operational source of truth for NotebookLM setup and use in the environment. Durable evaluation and rationale belong in the knowledge graph.

## Current Decision

NotebookLM is integrated as:

- an isolated local CLI tool
- a canonical shared skill
- an optional agent capability that delegates to the skill

It is not integrated as:

- a shared workspace secret
- a canonical data store
- a replacement for the knowledge graph

## Installation Standard

Install NotebookLM as an isolated tool with browser-login support:

```bash
rtk pipx install 'notebooklm-py[browser]'
```

Runtime command:

```bash
rtk notebooklm --help
```

Do not install it into a shared Python interpreter for this environment.

## Runtime State And Security

NotebookLM runtime state stays in user home:

- default home: `~/.notebooklm`
- auth file: `~/.notebooklm/storage_state.json`
- browser profile: `~/.notebooklm/browser_profile`

Required permissions:

- `~/.notebooklm` = `700`
- `~/.notebooklm/browser_profile` = `700`
- `~/.notebooklm/storage_state.json` = `600`

Do not move these files into `/mnt/c/Development`.
Do not commit or sync these files into Git, cloud backup, or dotfile repos.

## Authentication

Interactive login flow:

```bash
rtk notebooklm login
rtk notebooklm list
```

If login succeeds, `rtk notebooklm list` should stop reporting `Not logged in`.

For non-interactive or isolated workflows:

- use `NOTEBOOKLM_HOME` for per-agent or per-account state isolation
- use `NOTEBOOKLM_AUTH_JSON` only when a controlled non-interactive workflow requires it

## Canonical Skill Integration

The canonical shared skill is:

- `/mnt/c/Development/repos/infra/skills/skills/notebooklm/SKILL.md`

The live runtime path resolves through:

- `/mnt/c/Development/system/ai/skills`

Agents should use the skill rather than embedding NotebookLM usage instructions directly.

## Hermes Integration Rule

If Hermes is used as a shared environment agent, Hermes should:

- delegate NotebookLM behavior to the canonical `notebooklm` skill
- use NotebookLM for notebook-backed source-grounded synthesis
- file durable conclusions into the knowledge graph when they should survive the session
- avoid copying NotebookLM auth or browser state into workspace files

Hermes should not duplicate the complete NotebookLM command manual. The skill is the reusable interface.

## Source Of Truth Split

Use this model:

- NotebookLM = working synthesis over curated sources
- knowledge graph = conceptual and historical truth
- `system/docs/environment` = operational truth
- code and repos = executable truth

NotebookLM outputs are not automatically durable. If an output matters after the current task, synthesize it into the graph.

## Related

- `repos/infra/skills/skills/notebooklm/SKILL.md`
- `knowledge/Knowledge Graph/05 Research/Developer Tooling/NotebookLM CLI Evaluation.md`
- `system/docs/environment/hybrid-knowledge-workflow.md`
