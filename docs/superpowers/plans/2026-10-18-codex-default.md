# Codex Default Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Operate the existing job-search workflows through Codex in the requested public fork.

**Architecture:** A single portable skill routes to the original methodology; one runtime reference maps Claude tool names to Codex capabilities. A read-only Python preflight checks local dependencies without making provider calls or installing software.

**Tech Stack:** Markdown Agent Skills, Python 3.10+ standard library, existing Bun portal CLIs and LaTeX templates.

**Spec:** `docs/superpowers/specs/2026-10-18-codex-default-design.md`

## Global Constraints

- Codex is the default; preserve `.claude/`, `CLAUDE.md`, upstream history and MIT attribution.
- No new paid services, provider/model pins, global configuration changes, or personal data.
- Keep all original review, factuality, authorization and PDF-validation requirements.
- Runtime adapters use capabilities actually exposed in the session; never fabricate tool names or successful actions.

## Review Focus

- A fresh Codex session can discover the skill and route all upstream workflows.
- Public-fork onboarding warns before writing personal data into tracked templates.
- Missing Gmail/Notion access exits cleanly without writing state or requesting Claude installation.
- Missing reviewers/PDF capabilities are disclosed, never silently replaced with a claim of completion.
- Dependency reporting works from any directory, has deterministic exit codes, and does not expose credentials.

## Task 1: Codex entrypoint and runtime adapter

**Files:** `.agents/skills/job-search/{SKILL.md,agents/openai.yaml,references/codex-runtime.md}`, `AGENTS.md`, `tests/test_codex_workflows.py`.

**Interfaces:** Consumes original `.claude/commands/*.md` and two orchestration skills. Produces `$job-search <workflow> [arguments]` and a routing table of local Markdown links.

- [ ] Run a fresh-agent baseline for setup, absent Gmail connector, and absent reviewer.
- [ ] Add a routing-contract test: table keys equal upstream command stems plus scrape/upskill, every target exists, and each command resolves to its matching source. Run it and observe failure before adding the skill.
- [ ] Add the adapter and Codex instructions; validate skill metadata and route integrity.
- [ ] Replay the scenarios with the skill; preserve truthful unavailable-capability outcomes.
- [ ] Commit `feat: add Codex job-search workflow adapter`.

## Task 2: Read-only dependency preflight

**Files:** `tools/check_codex_setup.py`, `tests/test_check_codex_setup.py`.

**Interfaces:** `check_setup(workflow, *, find_executable, python_version)` returns checks with `name`, `available`, `required`, `hint`. CLI accepts `--workflow setup|scrape|apply|all` and `--json`; exit 0 iff required dependencies exist, else 1; invalid input exits 2.

- [ ] Test setup without Bun/TeX; scrape without Bun; apply with one missing TeX engine; missing Codex; Python below 3.10; all dependencies present; JSON and exit codes from a subprocess launched outside the repo with a controlled PATH.
- [ ] Observe RED, implement only dependency detection using the standard library, then verify GREEN.
- [ ] Optional PDF utilities are reported without blocking setup. No credentials, subprocess execution, network, or installation in the checker.
- [ ] Commit `feat: check local Codex workflow dependencies`.

## Task 3: Codex documentation and verification

**Files:** `README.md`, `SETUP.md`, `docs/upstream/{README.md,SETUP.md}`, `docs/codex-verification.md`.

**Interfaces:** Documents the skill and preflight above, preserves upstream documents with working relative links, and records reproducible verification commands.

- [ ] Make Codex the default quick start with actual `$job-search` syntax, public-template privacy, cost boundaries, optional integrations, and upstream updates.
- [ ] Run Python tests, skill validation, upstream lint/security guards, and portal fixture tests. Record skipped capabilities explicitly.
- [ ] Obtain a fresh-context review of the whole diff; fix material findings and rerun affected checks.
- [ ] Commit `docs: make Codex the default job-search workflow`.
- [ ] Inspect staged/history diffs and remote target; push small commits to origin/master and verify the remote SHA.
