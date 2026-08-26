# CLAUDE.md — Claude Code operating notes

**`AGENTS.md` is authoritative.** Read it first; everything there applies to you. This file adds only Claude-specific mechanics.

## Commands

Slash commands in `.claude/commands/` are thin adapters — each one points at a `skills/<name>/SKILL.md`, which is where all behavior lives. Available: `/setup`, `/capture`, `/draft`, `/process-transcript`, `/research`, `/apply`, `/ask`.

## Behavior

- **Commit after every run that writes files**, using the message format in AGENTS.md. Push if the remote is reachable; a failed push is not an error — the next run will push.
- **`/apply` is interactive by design.** It has exactly two human touchpoints (reflection and final review). Never skip the reflection pause; never submit anything anywhere.
- **Model routing:** skill frontmatter declares `cheap | mid | top` (see `specs/engineering-conventions.md` §4). Headless jobs are launched with the right model by `automation/run-job.sh`; interactively, just note when a task would benefit from `top`.
- **Before writing to `store/` or `people/`**, read `specs/store-conventions.md`. IDs are permanent; tags come from `store/tags.md`; unknown values are `{unknown}`.
- **Never** use web fetch/search with contents of `people/` or `memory/` files (names and companies are fine).

## Headless runs

Background jobs invoke `claude -p` via `automation/run-job.sh <job>`, with job prompts in `automation/jobs/`. If you are executing one of those prompts, you are non-interactive: flag ambiguities in the weekly digest instead of asking.
