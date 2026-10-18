---
framework_version: 1.0.1
---

# Agent Guidelines: AI Job Search

## Codex is the default runtime in this fork

For job-search tasks, load [.agents/skills/job-search/SKILL.md](.agents/skills/job-search/SKILL.md).
Use `$job-search <workflow> [arguments]` (for example `$job-search setup` or
`$job-search apply <posting URL or pasted text>`), or the equivalent natural-language
request. The skill routes to the original methodology without copying it.

When running in Codex, read the skill's
[runtime adapter](.agents/skills/job-search/references/codex-runtime.md) before
the selected workflow. Its tool mappings, connector preflights, and truthful
AI-tool attribution replace Claude-specific runtime instructions. The original
factuality, review, privacy, approval, and PDF checks still apply. The filename
`CLAUDE.md` is retained as the shared profile; it does not require Claude Code.

This is a public framework fork. Keep committed profiles as placeholders. Personal
setup is local/private work; never infer authorization to publish candidate data
from a request to generate a CV or update a profile. Do not install another AI
runtime or configure paid services to make a missing capability appear available.

For repository maintenance, preserve the original `.claude/` files and profile
format; update the Codex adapter when runtime behavior needs to differ. See
[SETUP.md](SETUP.md) for Codex installation and the local dependency check.

This workspace is structured to manage job search activities, scraper tools, CVs, cover letters, and interview preparation.

## Thin-Pointer Design (Single Source of Truth)

To prevent duplication and configuration drift across different AI agent frameworks (Claude Code, Google Antigravity, Codex, Cursor, Gemini CLI, etc.), this workspace uses a unified thin-pointer design. All agent runtimes should load the canonical specifications and candidate profiles from the files and directories below:

1. **Personal Candidate Profile:**
   - The candidate profile, contact details, education, and target preferences are defined in [CLAUDE.md](CLAUDE.md) and the individual profile methodology files under [.claude/skills/job-application-assistant/](.claude/skills/job-application-assistant/) (specifically `01-*.md` etc.).
2. **Canonical Workflow Specifications:**
   - The step-by-step instructions and triggers for tasks (setup, scrape, rank, apply, upskill, interview) are defined in the [.claude/](.claude/) directory (specifically under `.claude/skills/` and `.claude/commands/`).
   - Do not duplicate these rules or specifications. Treat `.claude/` files as the single source of truth.
3. **Portal Search Skills:**
   - Job-portal search CLIs live under [.agents/skills/](.agents/skills/) in the portable Agent Skills format (with a `SKILL.md` per portal). Codex and Antigravity discover these automatically; the `/scrape` workflow in [.claude/skills/job-scraper/](.claude/skills/job-scraper/) orchestrates them.
