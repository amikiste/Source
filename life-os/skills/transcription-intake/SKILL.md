---
name: transcription-intake
description: Transcript in, summary + decisions + action items out, filed onto the people involved.
commands: ["/process-transcript"]
writes: ["inbox/transcripts/processed/", "people/ (new files + #Notes + frontmatter)", "context/projects.md (dated bullets under existing headings)"]
model: mid
interactive: false
---

# Transcription intake — meetings into memory

## Purpose
Turn a meeting transcript from any tool (Granola, Fireflies, Gong, a voice memo, plain notes) into a clean summary, explicit decisions, and owner-assigned action items — then file the relevant history onto the people who were in the room, so the system knows them better every meeting.

## Inputs
- A transcript: a path given in `$ARGUMENTS`, pasted text, or (headless sweep) any unprocessed file in `inbox/transcripts/`.
- `people/` for recognizing participants; `context/projects.md` for recognizing project references.

## Steps
1. **Identify the meeting:** date (from file metadata or content; ask/flag if truly absent), participants, subject.
2. **Match participants** to `people/` per `specs/store-conventions.md` §6. Unknown participant → new file (`source: transcript`) with whatever the transcript establishes (company, role) — `{unknown}` elsewhere. Ambiguous match → ask (interactive) or flag (headless), never merge on a guess.
3. **Produce the summary file** at `inbox/transcripts/processed/YYYY-MM-DD-<subject-slug>.md`:
   - **Summary** — one tight paragraph
   - **Decisions** — bullet list, only real decisions
   - **Action items** — grouped by owner: `- [ ] <item> (owner: <name>, due: <date or none>)`
   - **Open questions** — anything left unresolved
4. **File to people:** each participant's `people/` file gets a dated note — their commitments, what they said that matters, anything that changes frontmatter (new role, new company). Update `last_touched`.
5. **File to projects:** meeting outcomes that belong to an existing `context/projects.md` heading get a dated bullet there.
6. **Move the source** transcript into `inbox/transcripts/processed/` alongside its summary (nothing is processed twice).

## Write-backs
Only surfaces in `writes:`. Appends only, dated. Commit: `transcript(<subject>): summary + <n> people updated`.

## Self-seed behavior
Missing `people/` or `inbox/transcripts/` → create and proceed.

## Failure behavior
Garbled or fragmentary transcript → process what's parseable, mark gaps `{inaudible/unclear}`, never reconstruct dialogue that isn't there. Headless ambiguities → note in the summary file under **Open questions** for digest pickup.
