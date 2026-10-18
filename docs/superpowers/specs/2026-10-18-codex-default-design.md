# Codex default workflow

## Intent

Make `dattk2002/mads-lorentzen-ai-job-search` a public fork that a Codex user can
operate without installing Claude Code. The user selected Codex as the default
while preserving upstream instructions to keep future updates manageable.

## Scope

- Keep the MIT license, upstream attribution, Git history, `.claude/`, and
  `CLAUDE.md`. These remain the canonical methodology and candidate-profile files.
- Add one discoverable `.agents/skills/job-search/SKILL.md` entrypoint. Use
  `$job-search <workflow> [arguments]`, routing to all existing commands plus the
  scrape and upskill skills. Do not duplicate the methodology or pretend Claude
  slash commands are registered in Codex.
- Define Codex tool mappings, native reviewer requirements, optional connector
  behavior, and missing-capability outcomes in one runtime reference.
- Add a read-only, standard-library Python dependency checker for setup, scrape,
  apply, and all workflows. Report executable presence, not successful execution.
- Make the README and SETUP default to Codex. Preserve original documents under
  `docs/upstream/`, with their relative links still working.
- Validate routing integrity, dependency-checker behavior, and realistic agent
  scenarios; retain upstream lint, security checks, and regression tests.

## Boundaries

No provider/model pinning, API keys, global Codex configuration changes, paid
services, personal profile population, application submission, email sending, or
new job-board integrations. Gmail and Notion remain optional. A missing reviewer
or PDF tool must not be reported as a completed reviewed application. Any public
commit contains templates and framework changes only.

## Implementation decisions

The single entrypoint and workflow-specific dependency checker are implementer
choices. Natural-language requests can select the same skill. The adapter takes
precedence only for runtime-specific syntax; upstream factuality, review, privacy,
approval, reset confirmation, and output-validation rules remain in force.

## Delivery

Use a fresh clone, preserve the upstream remote, make small coherent commits,
review the final diff, and push to the explicitly requested public fork. Report
checks performed and any unverified end-to-end capabilities.
