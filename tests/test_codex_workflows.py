"""Catch missing or misrouted upstream workflows in the Codex entrypoint."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".agents/skills/job-search/SKILL.md"


class CodexWorkflowRoutes(unittest.TestCase):
    def test_every_upstream_workflow_has_one_resolvable_route(self):
        self.assertTrue(SKILL.is_file(), "Codex needs a discoverable job-search skill")
        rows = re.findall(
            r"^\| `([^`]+)` \| \[[^]]+\]\(([^)]+)\) \|",
            SKILL.read_text(encoding="utf-8"), re.MULTILINE,
        )
        routes = dict(rows)
        self.assertEqual(len(rows), len(routes), "duplicate workflow names are ambiguous")
        expected = {
            path.stem: path.resolve()
            for path in (ROOT / ".claude/commands").glob("*.md")
        }
        expected.update({
            "scrape": ROOT / ".claude/skills/job-scraper/SKILL.md",
            "upskill": ROOT / ".claude/skills/upskill/SKILL.md",
        })
        self.assertEqual(set(routes), set(expected), "upstream workflow coverage drifted")
        for name, target in routes.items():
            with self.subTest(workflow=name):
                resolved = (SKILL.parent / target).resolve()
                self.assertEqual(resolved, expected[name])
                self.assertTrue(resolved.is_file())


if __name__ == "__main__":
    unittest.main()
