# Codex adapter verification

## Scope

The adapter preserves upstream methodology and changes the runtime bindings.
Executable detection and instruction dry runs are not evidence that a complete
personal application was generated. This record separates those checks.

## Checks performed on 2026-10-18

| Check | Result |
|---|---|
| Original Python baseline | 647 tests, 24 conditional skips, no failures |
| Python suite with Codex changes | 659 tests, 24 conditional skips, no failures |
| Portal CLI TypeScript checks | All six passed |
| Portal fixture/mock tests | 421 passed, no failures, no live portal requests |
| Skill validator | New `job-search` skill passed |
| Upstream skill/command lint | 10 skills, 12 commands, settings passed |
| Upstream security guards | Passed |
| Portal installer dry run | Discovered six portals; excluded workflow-only skill |
| Local dependency check | Setup available; stock PDF compilers absent |
| Codex CLI 0.163.0 read-only smoke | Discovered `$job-search`, loaded adapter and setup source |

The full Python run reports skipped tests explicitly. Upstream-only placeholder
checks and optional dependencies are conditional; a skip is not a passing test.

## Behavior checks

A fresh-agent baseline could not resolve `$job-search`, found the Claude-only
Gmail preflight, and found forced Claude Code attribution. With the adapter,
independent read-only dry runs selected the expected source and stopped correctly:

- Public-fork setup: privacy confirmation before onboarding/profile writes.
- Missing Gmail tools: exit before reading mail or creating state; no Claude setup.
- Missing Notion tools: exit without local or remote writes or OAuth.
- Missing reviewer/PDF compiler: disclose incomplete application checks; do not
  substitute self-review or fabricate a final PDF.
- Reset without typed `RESET`: inventory only; no deletion.
- AI-tool attribution: use confirmed candidate facts; never replace an unsupported
  Claude claim with an unsupported Codex claim.

A real `codex exec --ephemeral --sandbox read-only` smoke repeated discovery,
setup privacy, Gmail absence and attribution checks. It read instructions only.
The new dependency tests were observed failing before implementation and passing
afterward. The route test catches missing/upstream-added workflows and wrong
source paths. The scraper contract test now identifies portals by CLI manifests,
so names such as `job-search` do not turn orchestration into a phantom portal.

## Reproduce automated checks

```bash
python3 -m unittest discover -s tests -t . -v
python3 tools/lint_skills.py
python3 tools/security_guards.py
python3 tools/check_codex_setup.py --workflow all --json
python3 tools/install_portal_clis.py --dry-run
```

Install PyYAML for lint and `openpyxl` for Excel integration tests in your
development Python environment. For each `.agents/skills/*/cli` package, run:

```bash
bun install --ignore-scripts --no-save
bun run typecheck
bun test
```

For a read-only Codex smoke, open the repository in Codex and ask:

```text
Use $job-search setup as a read-only dry run. Do not start onboarding or write
files. The origin is a public fork. Identify the skill and canonical workflow,
then explain the confirmation needed before writing personal data. Also explain
what happens when Gmail tools are absent and how AI tooling is attributed in CVs.
```

## Not verified by these checks

- Full personalized setup → application → reviewed and visually verified PDFs:
  no personal profile was supplied, and local `lualatex`/`xelatex` were absent.
- Live Gmail/Notion synchronization: no account was connected or mutated for tests.
- Live portal availability: fixture tests validate parsing/contracts, not uptime.
- Other Codex clients and versions: the CLI smoke is evidence for the tested
  client; actual tool exposure, permissions and provider limits still vary.

No generated CV, candidate data, credentials or test session logs are part of the
published changes. Original `.claude/`, `CLAUDE.md`, document templates and license
remain unchanged from the upstream baseline.
