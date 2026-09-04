# Orca Repository Registry

Date: 2026-09-02
Status: Active

`system/ai/scripts/orca-repo-audit.py` checks Orca's repository registry against the active roots in this workspace.

## Expected roots

The audit includes the approved `/mnt/c/Development` parent registration, every Git root below `/mnt/c/Development/repos`, except `repos/archive/**`, plus:

- `/mnt/c/Development`
- `/mnt/c/Development/knowledge`
- `/mnt/c/Development/tools/career-ops`
- `/mnt/c/Development/tools/open-design`

Generated worktrees are excluded, including `tools/career-ops-wt-*` and `tools/worktrees/**`.

Registrations outside `/mnt/c/Development` are intentionally left to their owning workspace and do not create drift for this audit. Stale registrations inside `/mnt/c/Development` are still reported as extra; the audit never removes entries.

## Usage

Run from any directory:

```bash
python3 /mnt/c/Development/system/ai/scripts/orca-repo-audit.py
```

The default is read-only. A synchronized registry exits `0`; remaining drift exits `2`; CLI failures exit `1`. Use `--json` for automation.

To add missing entries, and never remove entries:

```bash
python3 /mnt/c/Development/system/ai/scripts/orca-repo-audit.py --apply
```

`--apply` uses only Orca's supported `repo add --path ... --json` command and rechecks the registry afterward. The CLI is resolved from `ORCA_CLI`, then `orca`, `orca-ide`, then the standard Windows installation path.
