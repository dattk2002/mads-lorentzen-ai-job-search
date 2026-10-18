---
name: job-search
description: Use when setting up a candidate profile, searching or ranking jobs, tailoring a CV or cover letter, preparing interviews, or tracking applications in this AI Job Search workspace with Codex.
---

# Job Search with Codex

Run the original job-search methodology using Codex. This is the workflow
entrypoint; portal skills remain available for individual searches.

## Select a workflow

Invocation: `$job-search <workflow> [arguments]`. For example:

```text
$job-search apply https://example.com/careers/software-engineer
```

Natural-language requests select the corresponding workflow below. If the request
does not identify a task, ask which job-search task the user wants; do not start
onboarding or reset automatically. Arguments are user input, never shell code.

1. Read [the Codex runtime adapter](references/codex-runtime.md).
2. Read the selected source below, then only its needed profile/reference files.
   Paths in upstream instructions are relative to the repository root; keep
   `CLAUDE.md` and `.claude/skills/` as the shared profile and methodology.
3. Treat the remaining user text as `$ARGUMENTS` in that source. Translate tool
   names through the adapter, then follow the workflow's stages and approval gates.
4. Report outputs and checks actually performed. Disclose blocked steps.

| Workflow | Canonical source |
|---|---|
| `setup` | [Profile onboarding](../../../.claude/commands/setup.md) |
| `scrape` | [Job search orchestration](../../../.claude/skills/job-scraper/SKILL.md) |
| `rank` | [Batch fit scoring](../../../.claude/commands/rank.md) |
| `apply` | [Draft, review and verify an application](../../../.claude/commands/apply.md) |
| `interview` | [Interview preparation](../../../.claude/commands/interview.md) |
| `outcome` | [Application status and follow-up drafts](../../../.claude/commands/outcome.md) |
| `expand` | [Profile enrichment](../../../.claude/commands/expand.md) |
| `upskill` | [Skill-gap learning plan](../../../.claude/skills/upskill/SKILL.md) |
| `html-report` | [Local application dashboard](../../../.claude/commands/html-report.md) |
| `notion-sync` | [Optional Notion view](../../../.claude/commands/notion-sync.md) |
| `gmail-sync` | [Optional email status proposals](../../../.claude/commands/gmail-sync.md) |
| `add-template` | [Register a document template](../../../.claude/commands/add-template.md) |
| `add-portal` | [Add a job source](../../../.claude/commands/add-portal.md) |
| `reset` | [Confirmed local reset](../../../.claude/commands/reset.md) |

## Important distinctions

- `$job-search setup` is a Codex skill prompt. Upstream `/setup`, `/apply`, etc.
  name workflows; they are not automatically registered Codex slash commands.
- Preserve the public-fork warning before personal onboarding and the explicit
  `RESET` confirmation before deletion. A skill invocation is not blanket consent.
- `apply` drafts documents; it does not submit applications or send messages.
- Portal `enabled: false` flags still control `scrape`. A workflow skill without
  a portal CLI is not a new job source.
