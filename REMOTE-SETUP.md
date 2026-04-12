# Remote Setup

Use separate remotes for:

- `/mnt/c/Development/knowledge`
- `/mnt/c/Development`

## Suggested Repository Names

- `development-knowledge`
- `development-environment`

## Add Remotes

```bash
rtk git -C /mnt/c/Development/knowledge remote add origin <knowledge-remote-url>
rtk git -C /mnt/c/Development remote add origin <environment-remote-url>
```

## First Push

```bash
rtk git -C /mnt/c/Development/knowledge push -u origin main
rtk git -C /mnt/c/Development push -u origin main
```

## Verify

```bash
rtk git -C /mnt/c/Development/knowledge remote -v
rtk git -C /mnt/c/Development remote -v
rtk git -C /mnt/c/Development/knowledge status --short
rtk git -C /mnt/c/Development status --short
```

## Notes

- The knowledge repo intentionally versions shared Obsidian vault configuration in addition to content.
- The environment repo versions environment governance files and `system/docs/environment`.
- Do not push `~/.codex`.
