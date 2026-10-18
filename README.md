<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Pip, the courier bird" width="160">
</p>

# AI Job Search with Codex

A **Codex-default fork** of [Mads Lorentzen's AI Job Search](https://github.com/MadsLorentzen/ai-job-search).
Set up your profile, find and rank jobs, tailor a CV and cover letter, and prepare
for interviews from a local workspace. **Claude Code is not required.**

This fork adds a native `$job-search` skill and a Codex runtime adapter. The
original `.claude/` methodology, `CLAUDE.md` profile, portal CLIs, templates and
Git history are preserved so improvements can still be brought in from upstream.
The old filename `CLAUDE.md` is shared profile data, not a runtime dependency.

Independent community fork maintained under `dattk2002`; not affiliated with
OpenAI or Anthropic. The original framework is by Mads Lorentzen and contributors.

## Quick start

### 1. Fork and clone

To use this fork locally:

```bash
git clone https://github.com/dattk2002/mads-lorentzen-ai-job-search.git
cd mads-lorentzen-ai-job-search
git remote add upstream https://github.com/MadsLorentzen/ai-job-search.git
```

To contribute your own framework changes instead, you can use
`gh repo fork dattk2002/mads-lorentzen-ai-job-search --clone` and set `gh`'s default
repository to your own fork before creating issues or PRs.

**This fork is public.** Setup writes personal data into tracked files, including
`CLAUDE.md` and profile/template files under `.claude/`. Keep personal changes local
or use a separate private repository before pushing them. See
[SETUP.md section 8](SETUP.md#8-pulling-upstream-updates-into-your-fork) for the
private-remote recipe. Public forks are for framework changes, not personal CVs.

### 2. Check prerequisites

Install [Codex](https://learn.chatgpt.com/docs/codex/cli), Python 3.10+, and
[Bun](https://bun.sh). For stock PDF templates, install LaTeX with `lualatex` and
`xelatex`; the [setup guide](SETUP.md) links platform-specific package instructions.

```bash
python3 tools/check_codex_setup.py --workflow setup
python3 tools/install_portal_clis.py
```

On Windows, use `py` or `python` if `python3` is unavailable. The dependency checker
does not install anything, read credentials or make network/AI calls. Its `apply`
and `all` modes check stock PDF compiler presence too.

### 3. Open Codex in this folder

```bash
codex
```

Inside Codex, enter:

```text
$job-search setup
```

You can import career documents, provide one CV, or answer onboarding questions.
The public-fork privacy check happens before personal profile writes.

### 4. Search and prepare an application

```text
$job-search scrape
$job-search rank
$job-search apply <posting URL or pasted job description>
```

These are **Codex skill prompts**, not terminal commands. Upstream `/setup` and
`/apply` syntax is not automatically registered as Codex slash commands. Natural
language such as “use the job-search skill to prepare for this interview” works too.

## Workflows

Use `$job-search` followed by:

| Workflow | Purpose |
|---|---|
| `setup` | Populate or update your candidate profile |
| `scrape` | Search enabled portal skills and deduplicate results |
| `rank` | Score the shortlist against your profile |
| `apply` | Evaluate fit, draft, obtain an independent review, verify PDFs |
| `interview` | Prepare for the current interview stage |
| `outcome` | Record application outcomes; draft follow-ups without sending |
| `expand` | Enrich your profile from supported source material |
| `upskill` | Identify skill gaps and learning priorities |
| `html-report` | Generate an offline HTML dashboard |
| `notion-sync` | Optional one-way view in a connected Notion database |
| `gmail-sync` | Optional email-based status proposals, approved before recording |
| `add-template` | Register another CV or cover-letter toolchain |
| `add-portal` | Add a public job-board search integration |
| `reset` | Reset selected local data after explicit `RESET` confirmation |

Portal search includes LinkedIn public listings and Freehire. The four Danish
portal examples ship disabled; setup can enable them for the appropriate market.
Public sources can be rate-limited or unavailable. If a posting cannot be fetched,
provide its full text; do not draft from a title alone.

## Capabilities and costs

- The repository and local tools have no subscription fee. AI work uses your
  existing Codex allowance or API billing. No Claude subscription is required.
- `apply` needs a Codex session with native subagents for the independent reviewer,
  a compiler for the chosen templates, and PDF inspection. Missing capabilities
  are reported; a partial draft is not presented as reviewed or ready to submit.
- Gmail and Notion are optional and use integrations available in your Codex
  session. The fork does not automatically install connectors or start OAuth.
- Adding another portal may involve a paid data service; that must be disclosed
  before configuration. No paid proxy is included by default.
- Applications and follow-up messages are drafted for your review, never sent
  just because you ran a job-search workflow.

## Files and upstream updates

| Location | Role |
|---|---|
| `AGENTS.md` | Codex entrypoint and repository instructions |
| `.agents/skills/job-search/` | Workflow router and runtime adapter |
| `.agents/skills/*/cli/` | Existing job-portal tools |
| `CLAUDE.md`, `.claude/skills/` | Shared candidate profile and methodology |
| `.claude/commands/` | Original workflow specifications |
| `documents/`, `cv/`, `cover_letters/` | Source material and application documents |
| `tools/check_codex_setup.py` | Read-only local prerequisite check |

Use the [Codex setup guide](SETUP.md) for installation, privacy, optional
connections and upstream updates. The [upstream README](docs/upstream/README.md)
and [upstream setup guide](docs/upstream/SETUP.md) retain the original Claude Code
instructions. For Codex, the [runtime adapter](.agents/skills/job-search/references/codex-runtime.md)
defines how those instructions are executed.

## Verification

Run `python3 -m unittest discover -s tests -t .`, `python3 tools/lint_skills.py`
(requires PyYAML), and `python3 tools/security_guards.py`. See
[verification notes](docs/codex-verification.md) for behavioral scenarios and
checks that require authenticated integrations or local PDF tools.

## License

[MIT](LICENSE). Original copyright and attribution are preserved. This fork does
not claim the original author's application outcomes as its own.
