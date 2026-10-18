"""Exercise dependency decisions and CLI exit codes without installed AI tools."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parent.parent / "tools/check_codex_setup.py"


class CodexSetupCheckTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "missing read-only Codex setup checker")
        spec = importlib.util.spec_from_file_location("check_codex_setup", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def check(self, workflow, installed, version=(3, 10)):
        return self.module.check_setup(
            workflow,
            find_executable=lambda name: f"/tools/{name}" if name in installed else None,
            python_version=version,
        )

    def missing(self, checks):
        return {item["name"] for item in checks if item["required"] and not item["available"]}

    def test_setup_does_not_require_bun_or_tex(self):
        self.assertEqual(self.missing(self.check("setup", {"codex"})), set())

    def test_scrape_requires_bun(self):
        self.assertEqual(self.missing(self.check("scrape", {"codex"})), {"bun"})

    def test_apply_requires_both_stock_pdf_engines(self):
        self.assertEqual(self.missing(self.check("apply", {"codex", "lualatex"})), {"xelatex"})

    def test_no_codex_is_a_blocker(self):
        self.assertEqual(self.missing(self.check("setup", set())), {"codex"})

    def test_python_version_floor_is_enforced(self):
        self.assertEqual(self.missing(self.check("setup", {"codex"}, (3, 9))), {"python"})

    def test_all_includes_search_and_pdf_tools(self):
        checks = self.check("all", {"codex", "bun", "lualatex", "xelatex"})
        self.assertEqual(self.missing(checks), set())
        self.assertTrue({"codex", "python", "bun", "lualatex", "xelatex"}.issubset(
            {item["name"] for item in checks if item["required"]}
        ))
        for item in checks:
            self.assertEqual(set(item), {"name", "required", "available", "hint"})

    def test_pdf_utilities_are_optional_and_visible(self):
        checks = self.check("apply", {"codex", "lualatex", "xelatex"})
        optional = {item["name"] for item in checks if not item["required"]}
        self.assertTrue({"pdftotext", "pdftoppm"}.issubset(optional))
        self.assertEqual(self.missing(checks), set())

    def test_unknown_workflow_is_rejected(self):
        with self.assertRaises(ValueError):
            self.check("typo", {"codex"})

    def run_cli(self, directory, args, installed=()):
        for name in installed:
            binary = directory / (name + (".exe" if os.name == "nt" else ""))
            # Deliberately not a real executable: detection must never run it.
            binary.write_text("not executable code\n", encoding="utf-8")
            binary.chmod(0o755)
        env = {**os.environ, "PATH": str(directory)}
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args], cwd=directory, env=env,
            capture_output=True, text=True, encoding="utf-8", timeout=10,
        )
        return result

    def test_json_cli_from_outside_repo_with_no_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(Path(tmp), ["--workflow", "all", "--json"])
        self.assertEqual(result.returncode, 1, result.stderr)
        body = json.loads(result.stdout)
        self.assertFalse(body["ready"])
        self.assertEqual(body["workflow"], "all")
        self.assertEqual(self.missing(body["checks"]), {"codex", "bun", "lualatex", "xelatex"})

    def test_cli_only_detects_binaries_without_executing_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(Path(tmp), ["--workflow", "setup", "--json"], ["codex"])
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ["codex.exe" if os.name == "nt" else "codex"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["ready"])

    def test_invalid_cli_workflow_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(Path(tmp), ["--workflow", "typo"])
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
