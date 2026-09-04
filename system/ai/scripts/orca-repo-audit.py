#!/usr/bin/env python3
"""Audit Orca's repository registry against the active Development roots."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from typing import Any, Callable, Iterable, Mapping, Sequence

WORKSPACE = Path("/mnt/c/Development")
REPOS_ROOT = WORKSPACE / "repos"
EXPLICIT_ROOTS = (
    WORKSPACE / "knowledge",
    WORKSPACE / "tools" / "career-ops",
    WORKSPACE / "tools" / "open-design",
)


def normalize_path(value: str | os.PathLike[str]) -> str:
    """Return a case-insensitive, separator-independent WSL path key."""
    raw = os.fspath(value).strip().replace("\\", "/")
    # Accept Windows drive paths emitted by Orca on a Windows host.
    if len(raw) >= 2 and raw[1] == ":" and raw[0].isalpha():
        raw = "/mnt/" + raw[0].lower() + raw[2:]
    elif raw.lower().startswith("//wsl.localhost/"):
        parts = raw.split("/")
        if len(parts) > 4:
            raw = "/" + "/".join(parts[4:])
    normalized = os.path.normpath(raw)
    return normalized.casefold()


def _excluded(path: Path, repos_root: Path, workspace: Path) -> bool:
    parts = path.parts
    if "archive" in parts and repos_root in path.parents:
        return True
    if "worktrees" in parts and workspace / "tools" in path.parents:
        return True
    return any(part.startswith("career-ops-wt-") for part in parts)


def _discover_expected_paths(workspace: Path) -> dict[str, str]:
    """Discover Git roots while excluding archives and generated worktrees."""
    repos_root = workspace / "repos"
    expected: dict[str, str] = {}
    # Development itself is intentionally registered for environment governance.
    expected[normalize_path(workspace)] = str(workspace)
    if repos_root.is_dir():
        for current, dirs, files in os.walk(repos_root, topdown=True):
            current_path = Path(current)
            dirs[:] = [d for d in dirs if not _excluded(current_path / d, repos_root, workspace)]
            if ".git" in dirs or ".git" in files:
                expected[normalize_path(current_path)] = str(current_path)
                # A Git root is the unit Orca registers. Avoid traversing its
                # generated/build contents; sibling roots remain discoverable.
                dirs[:] = []
    for path in (
        workspace / "knowledge",
        workspace / "tools" / "career-ops",
        workspace / "tools" / "open-design",
    ):
        expected[normalize_path(path)] = str(path)
    return expected


def discover_expected(workspace: Path = WORKSPACE) -> set[str]:
    return set(_discover_expected_paths(workspace))


def resolve_cli(env: Mapping[str, str] | None = None, which: Callable[[str], str | None] = shutil.which) -> list[str]:
    environment: Mapping[str, str] = os.environ if env is None else env
    override = environment.get("ORCA_CLI")
    if override:
        return shlex.split(override)
    for name in ("orca", "orca-ide"):
        found = which(name)
        if found:
            return [found]
    fallback = Path("/mnt/c/Users/mathe/AppData/Local/Programs/orca/resources/bin/orca.exe")
    if fallback.is_file():
        return [str(fallback)]
    raise FileNotFoundError("Orca CLI not found; set ORCA_CLI or install orca/ orca-ide")


def run_cli(cli: Sequence[str], args: Sequence[str]) -> Any:
    completed = subprocess.run([*cli, *args], text=True, capture_output=True, check=False)
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"Orca CLI failed ({completed.returncode}): {detail}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Orca returned invalid JSON: {exc}") from exc


def registry_paths(payload: Any) -> set[str]:
    if isinstance(payload, dict):
        payload = payload.get("result", payload)
        if isinstance(payload, dict):
            payload = payload.get("repos", [])
    if not isinstance(payload, list):
        raise RuntimeError("Orca repo list JSON did not contain a repository list")
    paths = set()
    for repo in payload:
        if isinstance(repo, dict) and isinstance(repo.get("path"), str):
            paths.add(normalize_path(repo["path"]))
    return paths


def audit(
    expected: Iterable[str],
    registered: Iterable[str],
    workspace: Path = WORKSPACE,
) -> dict[str, list[str]]:
    """Return workspace drift while ignoring registrations elsewhere."""
    workspace_key = normalize_path(workspace).rstrip("/")
    managed_registered = {
        path
        for path in registered
        if path == workspace_key or path.startswith(f"{workspace_key}/")
    }
    missing = sorted(set(expected) - set(registered))
    extra = sorted(managed_registered - set(expected))
    return {"missing": missing, "extra": extra}


def display_path(key: str) -> str:
    return key


def cli_path(path: str | os.PathLike[str]) -> str:
    """Convert WSL mount paths to native Windows paths for Orca's bridge."""
    raw = os.fspath(path).replace("\\", "/")
    if len(raw) >= 7 and raw[:5].lower() == "/mnt/" and raw[5].isalpha() and raw[6] == "/":
        return f"{raw[5].upper()}:{raw[6:].replace('/', chr(92))}"
    return os.fspath(path)


def main(argv: Sequence[str] | None = None, cli_runner: Callable[[Sequence[str], Sequence[str]], Any] = run_cli) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="add missing repositories; never removes entries")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable output")
    args = parser.parse_args(argv)
    try:
        cli = resolve_cli()
        expected_paths = _discover_expected_paths(WORKSPACE)
        expected = set(expected_paths)
        registered = registry_paths(cli_runner(cli, ("repo", "list", "--json")))
        drift = audit(expected, registered, WORKSPACE)
        added: list[str] = []
        if args.apply and drift["missing"]:
            for path in drift["missing"]:
                cli_runner(cli, ("repo", "add", "--path", cli_path(expected_paths[path]), "--json"))
                added.append(path)
            registered = registry_paths(cli_runner(cli, ("repo", "list", "--json")))
            drift = audit(expected, registered, WORKSPACE)
        result = {"expected": sorted(expected), "registered": sorted(registered), "missing": drift["missing"], "extra": drift["extra"], "added": added}
        if args.as_json:
            print(json.dumps(result, separators=(",", ":"), sort_keys=True))
        else:
            if not drift["missing"] and not drift["extra"]:
                print(f"Orca repository registry synchronized ({len(expected)} repositories).")
            else:
                print(f"Orca repository registry drift: {len(drift['missing'])} missing, {len(drift['extra'])} extra.")
                for path in drift["missing"]:
                    print(f"  missing: {display_path(path)}")
                for path in drift["extra"]:
                    print(f"  extra:   {display_path(path)}")
                if args.apply and added:
                    print(f"Added {len(added)} missing repositories; extra entries were not removed.")
        return 0 if not drift["missing"] and not drift["extra"] else 2
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        if args.as_json:
            print(json.dumps({"error": str(exc)}, separators=(",", ":"), sort_keys=True))
        else:
            print(f"orca-repo-audit: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
