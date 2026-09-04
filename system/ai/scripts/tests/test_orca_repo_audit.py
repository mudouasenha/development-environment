import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "orca-repo-audit.py"
spec = importlib.util.spec_from_file_location("orca_repo_audit", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OrcaRepoAuditTests(unittest.TestCase):
    def test_normalizes_windows_and_wsl_paths(self):
        self.assertEqual(module.normalize_path(r"C:\Development\Repos\Demo"), "/mnt/c/development/repos/demo")
        self.assertEqual(module.normalize_path("/mnt/c/Development/repos/demo/"), "/mnt/c/development/repos/demo")
        self.assertEqual(module.cli_path("/mnt/c/Development/repos/demo"), r"C:\Development\repos\demo")

    def test_discovers_expected_parent_git_roots_and_explicit_roots(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in (
                root / "repos" / "active",
                root / "repos" / "archive" / "old",
                root / "repos" / "career-ops-wt-1",
                root / "repos" / "nested",
                root / "tools" / "worktrees" / "generated",
            ):
                path.mkdir(parents=True)
                (path / ".git").mkdir()
            expected = module.discover_expected(root)
            self.assertIn(module.normalize_path(root), expected)
            self.assertIn(module.normalize_path(root / "repos" / "active"), expected)
            self.assertIn(module.normalize_path(root / "repos" / "nested"), expected)
            self.assertNotIn(module.normalize_path(root / "repos" / "archive" / "old"), expected)
            self.assertNotIn(module.normalize_path(root / "repos" / "career-ops-wt-1"), expected)
            self.assertNotIn(module.normalize_path(root / "tools" / "worktrees" / "generated"), expected)
            self.assertIn(module.normalize_path(root / "knowledge"), expected)

    def test_drift_is_sorted_and_ignores_external_registrations(self):
        workspace = Path("/mnt/c/Development")
        result = module.audit(
            {"/mnt/c/development", "/mnt/c/development/repos/active"},
            {"/mnt/c/development/repos/active", "/mnt/c/development/repos/stale", "/other/unmanaged/repo"},
            workspace,
        )
        self.assertEqual(result, {"missing": ["/mnt/c/development"], "extra": ["/mnt/c/development/repos/stale"]})

    def test_registry_paths_reads_orca_envelope(self):
        payload = {"result": {"repos": [{"path": r"C:\Development\Demo"}, {"path": "/mnt/c/Development/Other"}]}}
        self.assertEqual(module.registry_paths(payload), {"/mnt/c/development/demo", "/mnt/c/development/other"})

    def test_cli_resolution_order(self):
        which = lambda name: "/bin/orca-ide" if name == "orca-ide" else None
        self.assertEqual(module.resolve_cli({}, which), ["/bin/orca-ide"])
        self.assertEqual(module.resolve_cli({"ORCA_CLI": "orca --profile test"}, which), ["orca", "--profile", "test"])

    def _workspace(self, root):
        for path in (
            root / "knowledge",
            root / "tools" / "career-ops",
            root / "tools" / "open-design",
            root / "repos" / "known",
            root / "repos" / "missing",
        ):
            path.mkdir(parents=True)
        (root / "repos" / "known" / ".git").mkdir()
        (root / "repos" / "missing" / ".git").mkdir()

    def test_main_read_only_returns_two_without_add_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._workspace(root)
            original_workspace = module.WORKSPACE
            module.WORKSPACE = root
            try:
                expected = module.discover_expected(root)
                registered = expected - {module.normalize_path(root / "repos" / "missing")}
                registered.add("/external/unmanaged/repo")
                calls = []

                def runner(cli, args):
                    calls.append(tuple(args))
                    return {"result": {"repos": [{"path": path} for path in registered]}}

                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    status = module.main(["--json"], cli_runner=runner)
                result = json.loads(output.getvalue())
                self.assertEqual(status, 2)
                self.assertEqual(result["missing"], [module.normalize_path(root / "repos" / "missing")])
                self.assertEqual(result["extra"], [])
                self.assertEqual(len(calls), 1)
                self.assertFalse(any(args[:2] == ("repo", "add") for args in calls))
            finally:
                module.WORKSPACE = original_workspace

    def test_main_apply_adds_only_missing_and_rechecks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._workspace(root)
            original_workspace = module.WORKSPACE
            module.WORKSPACE = root
            try:
                expected_paths = module._discover_expected_paths(root)
                expected = set(expected_paths)
                missing = module.normalize_path(root / "repos" / "missing")
                registered = expected - {missing}
                calls = []

                def runner(cli, args):
                    calls.append(tuple(args))
                    if args[:3] == ("repo", "list", "--json"):
                        paths = registered if len([call for call in calls if call[:3] == ("repo", "list", "--json")]) == 1 else expected
                        return {"result": {"repos": [{"path": path} for path in paths]}}
                    self.assertEqual(args[:2], ("repo", "add"))
                    self.assertIn(args[3], expected_paths.values())
                    return {"ok": True}

                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    status = module.main(["--apply", "--json"], cli_runner=runner)
                result = json.loads(output.getvalue())
                self.assertEqual(status, 0)
                self.assertEqual(result["added"], [missing])
                self.assertEqual(result["missing"], [])
                self.assertEqual(result["extra"], [])
                self.assertEqual([call[:3] for call in calls].count(("repo", "list", "--json")), 2)
                self.assertEqual([call for call in calls if call[:2] == ("repo", "add")], [("repo", "add", "--path", str(root / "repos" / "missing"), "--json")])
                self.assertFalse(any(call[:2] == ("repo", "remove") for call in calls))
            finally:
                module.WORKSPACE = original_workspace

    def test_main_apply_passes_native_windows_path_to_runner(self):
        original_workspace = module.WORKSPACE
        original_discover = module._discover_expected_paths
        module.WORKSPACE = Path("/mnt/c/Development")
        module._discover_expected_paths = lambda workspace: {
            "/mnt/c/development": "/mnt/c/Development",
            "/mnt/c/development/repos/missing": "/mnt/c/Development/repos/missing",
        }
        calls = []
        try:
            def runner(cli, args):
                calls.append(tuple(args))
                if args[:3] == ("repo", "list", "--json"):
                    paths = ["/mnt/c/Development"] if len(calls) == 1 else [
                        "/mnt/c/Development", "/mnt/c/Development/repos/missing"
                    ]
                    return {"result": {"repos": [{"path": path} for path in paths]}}
                return {"ok": True}

            self.assertEqual(module.main(["--apply"], cli_runner=runner), 0)
            self.assertIn(
                ("repo", "add", "--path", r"C:\Development\repos\missing", "--json"),
                calls,
            )
        finally:
            module.WORKSPACE = original_workspace
            module._discover_expected_paths = original_discover


if __name__ == "__main__":
    unittest.main()
