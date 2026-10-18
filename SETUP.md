# Codex Setup Guide

This fork runs through Codex. Keep `.claude/` and `CLAUDE.md`: their filenames are
retained for upstream compatibility, and the Codex skill reads them as methodology
and profile data. You do not need to install Claude Code or Gemini CLI.

## 1. Prerequisites

Install or update [Codex CLI](https://learn.chatgpt.com/docs/codex/cli), then sign
in using your existing account or API setup. Start with your existing model;
this repository does not pin a model, set API keys, or change global permissions.
Codex desktop/IDE sessions can use the same repo-local skill when they have file
and terminal access; the checker below specifically checks the CLI executable.

Install Python 3.10+ and [Bun](https://bun.sh). On Windows, replace `python3` with
`py` or `python` if needed. The stock CV requires `lualatex`; stock cover letters
require `xelatex`. Use the preserved upstream instructions for
[TeX prerequisites](docs/upstream/SETUP.md#latex-for-compiling-cvs-and-cover-letters),
[TinyTeX/BasicTeX packages](docs/upstream/SETUP.md#minimal-tex-install-tinytexbasictex),
and [Windows MiKTeX](docs/upstream/SETUP.md#windows-basic-miktex).

For PDF text checks, install `pypdf` in your Python environment or use Poppler's
`pdftotext`. Poppler's `pdftoppm` can render pages for visual inspection. PDF
rendering and text extraction are separate checks; neither replaces the other.

## 2. Fork and clone

For local use, clone directly:

```bash
git clone https://github.com/dattk2002/mads-lorentzen-ai-job-search.git
cd mads-lorentzen-ai-job-search
git remote add upstream https://github.com/MadsLorentzen/ai-job-search.git
```

For contributing framework changes, run:

```bash
gh repo fork dattk2002/mads-lorentzen-ai-job-search --clone
gh repo set-default <your-github-username>/mads-lorentzen-ai-job-search
```

**Forks are public.** Setup writes personal data into tracked files. For a personal
job search, keep those changes local or use the private-remote recipe in
[section 8](#8-pulling-upstream-updates-into-your-fork). Never push personalized
templates to this public framework repository. The public-fork check will ask for
confirmation before onboarding writes.

## 3. Check tools and install portal dependencies

```bash
python3 tools/check_codex_setup.py --workflow setup
python3 tools/check_codex_setup.py --workflow scrape
python3 tools/check_codex_setup.py --workflow apply
python3 tools/install_portal_clis.py
```

The preflight exits `0` when required prerequisites are found, `1` when something
required is missing, and `2` for invalid arguments. `--json` prints a structured
report. The default workflow is `all`. It only detects executables: it does not
test sign-in, subagent availability, TeX packages/fonts, or connectors. `apply`
checks the **stock** templates; a custom template uses its own registered compiler.
The `apply` workflow can fetch known portal URLs through Bun when available and
otherwise use the session's web tools or a pasted description.

The portal installer discovers `cli/package.json` files. It will not treat the
new `job-search` orchestration skill as a portal. LinkedIn and Freehire have no
runtime npm dependencies and can run directly with Bun.

## 4. Start Codex and set up your profile

```bash
codex
```

In the Codex conversation:

```text
$job-search setup
```

The skill supports the original three onboarding paths: material under
`documents/`, one pasted/referenced CV, or an interview. Check proposed facts
carefully. No profile facts are inferred from this fork owner's GitHub identity.

To update one part later:

```text
$job-search setup --section skills
$job-search setup --section search
```

If the skill is absent, run `/skills` or restart Codex in the repository root.
It lives at `.agents/skills/job-search/SKILL.md`. Do not copy the entire repo into
your global skills directory. See [Codex skills](https://learn.chatgpt.com/docs/build-skills).

## 5. Search, rank and apply

```text
$job-search scrape
$job-search rank
$job-search apply <posting URL or full job description>
```

The adapter maps upstream tool names to the tools actually exposed by Codex.
An application is complete only after independent review and successful document
verification. If subagents are unavailable, continue in a capable Codex session;
the workflow will not silently substitute self-review or run another AI CLI.
See [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
for the configuration supported by your version. This fork does not overwrite it.

For another document format, use `$job-search add-template`. Salary benchmarking
is optional and reads your own local data; see [the salary tool](tools/README_SALARY_TOOL.md).

## 6. Optional integrations

`$job-search html-report` produces a local dashboard without an external account.
`$job-search outcome` tracks status locally; follow-ups remain drafts.

`$job-search gmail-sync` needs a Gmail connection offering search and full
message/thread reads in your Codex session. With no connection, it stops without
creating state. It proposes status updates with source-email references and waits
for approval before changing the local tracker. It does not send email.

`$job-search notion-sync` needs an existing Notion connection with search, database
and page operations. It resolves the destination before writes and keeps repo files
as the source of truth. Connect integrations separately through your supported
Codex client or established tools. Do not follow the archived Claude connector
installation commands for Codex.

Missing integrations do not block setup, search, CV drafting or local tracking.
Your provider/connector's limits apply; nothing in this fork purchases a service.

## 7. Verify the installation

```bash
python3 tools/check_codex_setup.py
python3 -m unittest discover -s tests -t .
python3 tools/lint_skills.py
python3 tools/security_guards.py
```

The linter needs PyYAML, and Excel integration tests need `openpyxl`; install
these in your development Python environment if needed. Portal fixture tests run
with `bun test` inside each `.agents/skills/<portal>/cli/` directory after installing
its development dependencies. These tests do not make live job-board requests.

For actual PDF readiness, compile the example CV and cover letter using the
[upstream smoke commands](docs/upstream/SETUP.md#minimal-tex-install-tinytexbasictex),
then inspect both rendered documents. Merely finding `lualatex` on PATH does not
prove fonts or packages are installed. See [verification notes](docs/codex-verification.md).

## 8. Pulling upstream updates into your fork

### Personal work: private remote first

If you want remote backup for personalized profiles, create a separate **private**
repository. From a fresh clone of this public fork, with no existing private origin:

```bash
git remote rename origin public-fork
gh repo create <your-github-username>/my-job-search --private --source=. --remote=origin
gh repo set-default <your-github-username>/my-job-search
git remote -v
```

Verify the new origin is private before committing and pushing personal material.
Review exactly what is staged; ignored documents are not a substitute for checking
tracked profile/template changes. Keeping commits local without pushing is fine.

### Framework updates

Keep `upstream` pointed at `https://github.com/MadsLorentzen/ai-job-search.git`.
If it is absent, add it once with `git remote add upstream <URL>`. Before merging:

```bash
git fetch upstream --tags
python3 tools/check_upstream_updates.py
python3 tools/upstream_triage.py --remote upstream --branch master
```

Prefer a reviewed upstream release tag. Resolve conflicts by retaining this fork's
Codex entrypoint/adapter and your own profile while adopting methodology updates.
Run tests and lint after updating: the routing test catches newly added commands
that are missing from the Codex skill. Never overwrite a personalized profile with
the stock template to make an update apply.

The [archived upstream setup guide](docs/upstream/SETUP.md) provides the original
Claude reference workflow. In this fork, use `$job-search <workflow>` and the
[Codex runtime adapter](.agents/skills/job-search/references/codex-runtime.md).
