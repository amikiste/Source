# life-os

Charlie Fleet's personal AI system: background, memories, voice, people, and career knowledge stored as plain markdown in this private repo — maintained by AI skills, owned by Charlie, independent of any AI provider's memory.

## Quick start

1. Clone this repo, open it in Claude Code (or any capable agent — see `AGENTS.md`).
2. First time: run `/setup`. It interviews you and seeds your memory files.
3. Daily use:
   - `/capture <anything>` — file a thought, task, link, or name
   - `/draft <request>` — write something in your voice
   - `/process-transcript` — turn a meeting transcript into a summary + filed notes
   - `/research <topic>` — quick sourced answer; `--brief` for a full company sheet; `prep <person>` before a call
   - `/apply <posting>` — full application package (six work products, two touchpoints)
   - `/ask <question>` — ask anything about your own history
4. Background automation (optional): see `automation/README.md`.

## Layout

| Path | What |
|---|---|
| `AGENTS.md` / `CLAUDE.md` | Agent entry points (any runtime / Claude Code) |
| `PRD.md`, `specs/` | The ratified design and the four governing specs |
| `context/`, `people/`, `memory/` | Shared memory (the compose contract) |
| `store/` | Career knowledge base (agent-maintained, stable IDs) |
| `skills/` | The suite — one folder per skill, plain markdown |
| `.claude/commands/` | Slash-command adapters |
| `applications/`, `research/` | Generated work products and briefs |
| `inbox/` | Drop zone: transcripts, postings, external research |
| `automation/` | Background jobs: wrappers, prompts, schedules |

## Status

Scaffold (PRD Phase 2). Next: ratify `specs/store-conventions.md`, then run the Phase 3 bootstrap (`/setup`, then the store bootstrap described in `PRD.md` §13) on a machine with access to the OneDrive archive and LinkedIn export.
