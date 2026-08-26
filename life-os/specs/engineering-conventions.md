# Workstream D — Engineering & Repo Conventions Spec
**Status:** Draft for ratification
**Governs:** repo mechanics: entry points, adapters, git policy, model routing, scheduling, contract governance.

## 1. Entry points

- **`AGENTS.md`** (repo root) is the canonical entry for *any* agent: what the repo is, the compose contract rules, the skill index, and the invocation protocol ("to run a skill, read `skills/<name>/SKILL.md` and follow it"). Provider-neutral; no Claude-specific syntax.
- **`CLAUDE.md`** is Claude Code's operating file: points to `AGENTS.md` as authoritative, then adds Claude-specific notes (available slash commands, permissions posture, commit behavior).
- **`.claude/commands/<cmd>.md`** are thin adapters, ≤10 lines each: name the skill file, pass `$ARGUMENTS`, nothing else. All behavior lives in the SKILL.md so every runtime executes identical logic.

## 2. Skill file conventions

`skills/<name>/SKILL.md` with YAML frontmatter:

```yaml
---
name: research
description: Tiered research - quick sourced answers or full company briefs
commands: ["/research"]
writes: ["research/", "people/*.md#Notes", "people/ (new files)"]
model: mid        # cheap | mid | top - a routing hint, not a hard bind
interactive: false # true = requires human touchpoints; never scheduled headless
---
```

Body sections in fixed order: **Purpose → Inputs → Steps → Write-backs → Self-seed behavior → Failure behavior.** The `writes:` list is the enforceable contract surface (§5.2 of the PRD); hygiene can lint a skill run's diff against it.

## 3. Git policy

- **Main-only.** No branches in steady state; a single user with append-mostly files makes conflicts rare. (Agents building *changes to the system itself* — new skills, spec revisions — may use short-lived branches.)
- **Commit messages:** `<skill>(<subject>): <what>` — e.g., `apply(acme-health): six work products + 2 insights`, `hygiene: fix 3 dangling tags`. Background jobs prefix with `[auto]`.
- **Every skill run that writes, commits.** Push if a remote is reachable; if push fails, commit locally and let the next run push (wrappers retry with backoff).
- **Background jobs:** `git pull --rebase` before running; if rebase fails, abort the run and flag in the digest — never force-push, never auto-resolve conflicts.
- **Recovery drill:** a bad auto-commit is reverted with `git revert` (history preserved), never reset. The weekly digest lists all `[auto]` commits for passive review.

## 4. Model routing

| Class | Used for | Example |
|---|---|---|
| `cheap` | Background jobs, parsing, sweeps, hygiene | Haiku-class |
| `mid` | Interactive research, drafting, transcripts, /apply pipeline | Sonnet-class |
| `top` | Deep briefs and positioning for priority targets, on request | Opus-class |

The class lives in skill frontmatter; wrappers map class → concrete model flag in one place (`automation/run-job.sh`), so upgrading models is a one-line change. A `--model top` override is always available interactively.

**Multi-model quality loop (v1.0 open question 15):** optional, manual in v1 — Charlie may drop a Gemini/Copilot critique into `inbox/research-drops/` and any skill will treat it as a source. Formalizing an automatic cross-model review step is deferred until dry runs show where quality actually sags.

## 5. Scheduling & notifications

- **One designated scheduler machine** (the Mac that's most reliably awake). Other machines run skills interactively only — this removes same-job-twice conflicts by policy rather than locking. If the designated machine changes, move the plists; the repo carries them.
- launchd plists in `automation/` (macOS primary); equivalent cron lines documented for Linux.
- **Notifications:** macOS Notification Center for immediate signals (job failure, pulse-check flag); the weekly digest is a file plus one notification. Email/Slack channels are a later addition if notification fatigue or absence becomes real.
- All job output logs to `_cache/logs/<job>-YYYY-MM-DD.log` (gitignored, 30-day retention).

## 6. Reflection prompt design (v1.0 open question 14)

Hybrid: the agent **proposes 2–3 candidate connections** it found in the store (each citing entity IDs), *then* asks the open question — "Do any of these ring true? Anything else in your history that particularly connects you to this role?" Rationale: pure open-ended wastes the store's knowledge; pure multiple-choice caps the insight the flywheel exists to capture. Confirmed or novel connections both write to `store/insights.md`.

## 7. Contract governance

- `.compose-contract` records `contract: v1.1`.
- A new skill that needs a **new shared surface** (a new folder or a new writable section in an existing shared file) requires: bump the contract version, update `AGENTS.md`'s contract summary, and note the migration in the changelog section of `.compose-contract`. Skills that only add their own folder need nothing.
- Remix-built v1 components remain compatible (they ignore `memory/` and `store/`).

## 8. Secrets & environment

- `.env` (gitignored) holds anything secret; `.env.template` documents every variable with a placeholder. v1 needs no API keys beyond the Claude subscription; the template exists so later additions (e.g., a notification webhook) have a home.
- No secret ever appears in a skill file, a log, or a commit.
