#!/usr/bin/env python3
"""Read-only executable checks for the stock Codex job-search workflows.

This detects local prerequisites only. It never executes an AI CLI, installs
packages, opens a connection, or reads credentials. TeX packages/fonts, Codex
authentication, subagent access and connector availability need session checks.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys

WORKFLOWS = ("setup", "scrape", "apply", "all")


def check_setup(workflow, *, find_executable=shutil.which, python_version=None):
    """Return prerequisite checks for a workflow without executing dependencies."""
    if workflow not in WORKFLOWS:
        raise ValueError(f"Unknown workflow: {workflow}")
    version = sys.version_info[:2] if python_version is None else python_version[:2]
    checks = [{
        "name": "python", "available": tuple(version) >= (3, 10), "required": True,
        "hint": "Run this checker with Python 3.10 or newer.",
    }]
    tools = [("codex", True, "Install Codex CLI, then sign in separately; see SETUP.md.")]
    if workflow in ("scrape", "all"):
        tools.append(("bun", True, "Install Bun for the portal CLIs; see SETUP.md."))
    if workflow in ("apply", "all"):
        tools.extend([
            ("lualatex", True, "Install LuaLaTeX and the stock CV packages; see SETUP.md."),
            ("xelatex", True, "Install XeLaTeX and the stock letter packages; see SETUP.md."),
            ("pdftotext", False, "Poppler extracts PDF text; pypdf is an alternative."),
            ("pdftoppm", False, "Poppler renders PDF pages; native PDF viewing is an alternative."),
        ])
    for name, required, hint in tools:
        checks.append({
            "name": name, "available": find_executable(name) is not None,
            "required": required, "hint": hint,
        })
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", choices=WORKFLOWS, default="all")
    parser.add_argument("--json", action="store_true", help="Output a JSON report")
    args = parser.parse_args(argv)
    checks = check_setup(args.workflow)
    ready = all(check["available"] for check in checks if check["required"])
    if args.json:
        print(json.dumps({"workflow": args.workflow, "ready": ready, "checks": checks}))
    else:
        print(f"Codex prerequisites: {args.workflow}")
        for check in checks:
            status = "found" if check["available"] else "missing"
            requirement = "required" if check["required"] else "optional"
            print(f"  {check['name']}: {status} ({requirement})")
            if not check["available"]:
                print(f"    {check['hint']}")
        print("Required executables found." if ready else "Required prerequisites are missing.")
        print("Presence only: sign-in, subagents, connectors, TeX packages and PDF rendering are not tested.")
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())
