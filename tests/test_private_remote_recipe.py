"""Execute the guide's Git steps against local remotes to prevent public pushes."""

import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest

GUIDE = Path(__file__).resolve().parent.parent / "SETUP.md"


@unittest.skipUnless(shutil.which("git"), "requires git")
class PrivateRemoteRecipeTests(unittest.TestCase):
    def test_plain_push_after_private_setup_never_changes_public_remote(self):
        section = GUIDE.read_text(encoding="utf-8").split(
            "### Personal work: private remote first", 1
        )[1]
        recipe = re.search(r"```bash\n(.*?)```", section, re.DOTALL).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public, private, seed, work = [root / name for name in (
                "public.git", "private.git", "seed", "work"
            )]
            env = {
                **os.environ, "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull, "GIT_TERMINAL_PROMPT": "0",
                "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            }

            def git(cwd, *args):
                result = subprocess.run(
                    ["git", *args], cwd=cwd, env=env, capture_output=True,
                    text=True, encoding="utf-8", timeout=20,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout.strip()

            for destination in (public, private):
                git(root, "init", "--bare", "--initial-branch=master", str(destination))
            git(root, "init", "--initial-branch=master", str(seed))
            (seed / "profile.txt").write_text("template\n", encoding="utf-8")
            git(seed, "add", "profile.txt")
            git(seed, "commit", "-m", "Template fixture")
            git(seed, "remote", "add", "origin", str(public))
            git(seed, "push", "-u", "origin", "master")
            baseline = git(public, "rev-parse", "master")
            git(root, "clone", str(public), str(work))

            for line in recipe.splitlines():
                args = shlex.split(line)
                if not args or args[0].startswith("#"):
                    continue
                if args[:3] == ["gh", "repo", "create"]:
                    # GH provisioning is outside this Git regression: use a
                    # real local bare repo and reproduce its origin creation.
                    git(work, "remote", "add", "origin", str(private))
                elif args[:3] in (["gh", "repo", "set-default"], ["gh", "repo", "view"]):
                    continue
                else:
                    self.assertEqual(args[0], "git", "unexpected command in recipe")
                    git(work, *args[1:])

            (work / "profile.txt").write_text("synthetic private candidate\n", encoding="utf-8")
            git(work, "add", "profile.txt")
            git(work, "commit", "-m", "Personal fixture")
            personal = git(work, "rev-parse", "HEAD")
            git(work, "push")
            self.assertEqual(git(public, "rev-parse", "master"), baseline,
                             "plain git push published personalized data to the public fork")
            self.assertEqual(git(private, "rev-parse", "master"), personal)
            self.assertEqual(git(work, "rev-parse", "--abbrev-ref", "@{upstream}"), "origin/master")


if __name__ == "__main__":
    unittest.main()
