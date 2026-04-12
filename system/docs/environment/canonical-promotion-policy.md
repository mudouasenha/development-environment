# Canonical Promotion Policy

Date: 2026-04-11
Status: Active

## Purpose

Define how assets move between:

- canonical shared roots under `/mnt/c/Development/system/ai`
- imported source roots under `/mnt/c/Development/system/ai/sources`
- user-scoped runtime state under `~/.codex`

This policy exists to prevent the environment from drifting back into split ownership.

## Core Rule

Canonical assets live in one place only.

For the current setup, that means:

- canonical shared skills: `/mnt/c/Development/system/ai/skills`
- canonical shared agents: `/mnt/c/Development/system/ai/agents`
- canonical shared plugin bundles: `/mnt/c/Development/system/ai/plugins/shared/*`

For skills specifically:

- authored canonical source: `/mnt/c/Development/repos/infra/skills`
- deployed runtime path: `/mnt/c/Development/system/ai/skills`

The deployed runtime path may be a symlink to the authored source. Treat the authored repo as the place where canonical skill edits should happen.

Imported or cached material must not be treated as canonical until it is explicitly promoted.

## Asset Classes

### Canonical

Use canonical roots for assets that are:

- actively used in the shared environment
- intended to be versioned as the long-term source of truth
- stable enough to be shared across projects or sessions
- intentionally curated rather than passively mirrored

Current canonical examples:

- workspace shared skills from `.agents/skills/skills`
- promoted Codex `.system/*` skills
- promoted `gsd-*` skills
- shared agent definitions under `system/ai/agents`

### Imported

Use imported roots for assets that are:

- upstream references
- third-party packages
- local caches or mirrors
- user-level overlays not yet approved for promotion
- overlapping skill packs that may conflict with canonical content

Current imported examples:

- `anthropic-skills`
- `.net-skills`
- full `codex-user-skills`
- cached Notion plugin package

### Runtime-Only

Keep runtime-only state in user home. Do not migrate it into the shared workspace.

Examples:

- `~/.codex/auth.json`
- `~/.codex/.credentials.json`
- `~/.codex/sessions`
- `~/.codex/cache`
- `~/.codex/log`
- `~/.codex/tmp`
- approval memory and local state databases

## Promotion Rules

Promote an imported or user-level asset into canonical only when all of these are true:

1. It is needed in normal shared use, not just one user’s local workflow.
2. It does not duplicate or conflict with an existing canonical asset without an explicit replacement decision.
3. Its source and provenance are recorded in the registry.
4. The promotion is intentional and documented in environment docs.
5. The promoted version becomes the maintained source of truth after promotion.

If any of those are false, keep the asset in `sources/*`.

## Promotion Process

1. Identify the candidate asset in `sources/*` or a user-level root.
2. Check for overlap with existing canonical assets.
3. Decide whether this is:
   - additive promotion
   - replacement promotion
   - keep imported only
4. Copy or sync into the canonical root.
5. Update registry metadata.
6. Update environment documentation if behavior changes.
7. Re-run `verify-links.sh` if the promotion affects live Codex use.

## Replacement Rules

If a promoted asset replaces an existing canonical asset:

- do not silently overwrite by convention alone
- document the replacement decision
- preserve the replaced source path in provenance notes
- verify that the runtime still resolves the expected skills, agents, or plugins

## Anti-Rules

Do not:

- treat plugin cache as canonical
- merge the full `~/.codex/skills` tree into canonical by default
- move secrets or session state into `/mnt/c/Development`
- let tool-specific directory layouts redefine canonical structure
- promote imported assets just because they exist

## Current Decisions

These decisions are already in force:

- `.agents/skills/skills` is the canonical base for shared skills
- `~/.codex/skills/.system/*` and `gsd-*` are promoted into canonical
- `anthropic-skills`, `.net-skills`, and the full `codex-user-skills` tree remain imported
- Notion plugin cache remains imported, not canonical

## Review Trigger

Revisit this policy when:

- a new tool is cut over into the shared environment
- a large new imported skill pack is added
- canonical and imported assets begin to overlap significantly
- a shared team workflow depends on assets still living only in user home
