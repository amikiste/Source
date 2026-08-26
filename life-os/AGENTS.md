# life-os — Agent Operating Guide

This repository is Charlie Fleet's personal AI system: his background, memories, voice, people, and career knowledge as plain markdown, plus a suite of skills that read and maintain it. It is the single system of record. **No AI provider's memory feature is ever used** — everything an agent needs to know lives in these files.

This file is the canonical entry point for any agent, regardless of vendor or runtime. If you can read files, you can operate this repo.

## How to run a skill

1. Read `skills/<name>/SKILL.md`.
2. Follow it exactly. Each skill declares its purpose, inputs, steps, write surfaces, self-seed behavior, and failure behavior.
3. Commit your changes when done (see Git rules below).

| Skill | Command | What it does |
|---|---|---|
| `skills/setup` | `/setup` | Onboarding interview; seeds `context/` and `memory/`. Re-runnable. |
| `skills/capture` | `/capture <anything>` | Files a thought, task, link, or name where it belongs. |
| `skills/writer-voice` | `/draft <request>` | Drafts prose in Charlie's voice; learns from edits. |
| `skills/transcription-intake` | `/process-transcript [file]` | Transcript → summary + decisions + action items, filed by person. |
| `skills/research` | `/research <topic>` / `--brief` / `prep <person>` | Quick sourced answers, full company briefs, meeting prep. |
| `skills/career-application-engine` | `/apply <posting>`, `/ask <question>` | Six application work products with two human touchpoints; ad-hoc career inquiry. |

Slash commands are Claude Code adapters in `.claude/commands/`; other runtimes invoke skills by reading the SKILL.md directly (e.g., "run the research skill on Acme Corp").

## The memory (shared surfaces)

| Surface | Contents | Who writes |
|---|---|---|
| `context/you.md` | Identity, role, working style | setup; human |
| `context/voice.md` | Writing rules, samples, `## Learned` | writer-voice appends to Learned only |
| `context/projects.md` | Active projects and campaigns | capture, setup |
| `people/<name>.md` | One file per person: frontmatter + `## Notes` | transcription-intake, research, capture, apply |
| `memory/` | Background, preferences, dated journal | setup, capture |
| `store/` | Career knowledge base (positions, accomplishments, insights, ...) | career-application-engine, hygiene job |
| `applications/`, `research/` | Work products and briefs | their owning skills |
| `inbox/` | Human drop zone (transcripts, postings, research files) | human drops; skills consume |

## The compose contract (v1.1 — see `.compose-contract`)

1. **Read freely.** Any skill may read any shared surface to personalize output.
2. **Write narrowly.** Write only to the surfaces your SKILL.md declares under `writes:`.
3. **Append, never clobber.** Shared-file writes are additive and dated. Human-authored content is sacred. Store entities use stable IDs (`{pos-001}` style — see `specs/store-conventions.md`); never delete or renumber.
4. **Self-seed if missing.** A fresh clone must never make a skill fail; create the minimal stubs you need.
5. **Stub, don't assume.** Unknown values are `{unknown}` or `{add role}` — visible placeholders, never invented facts.
6. **Commit with readable messages.** Format: `<skill>(<subject>): <what>`. Background jobs prefix `[auto]`. Pull before writing when possible; never force-push.

## Sensitivity rules

- `people/` and `memory/` are the most sensitive content. Never quote their contents into web searches or any external service. Public names + companies in a search: fine. Note contents: never.
- Secrets live only in `.env` (gitignored). Never write a secret to any tracked file or log.

## Where things are specified

- `PRD.md` — the ratified product definition (v2.1)
- `specs/store-conventions.md` — store formats, IDs, tags, people schema **(read before writing to `store/` or `people/`)**
- `specs/research-spec.md` — research tiers, brief template, source standards
- `specs/work-product-templates.md` — the six application products
- `specs/engineering-conventions.md` — git policy, model routing, scheduling, governance
