model: mid

You are running headless in the life-os repo (read `AGENTS.md` for the rules; you cannot ask questions — flag ambiguities instead).

Task: process any unprocessed meeting transcripts.

1. List files in `inbox/transcripts/` (excluding the `processed/` subfolder). If none, exit saying "nothing to process".
2. For each file, execute `skills/transcription-intake/SKILL.md` in headless mode: summary file to `inbox/transcripts/processed/`, dated notes onto the participants' `people/` files, project bullets where they belong, source file moved to `processed/`.
3. Ambiguous person matches or missing dates: record under **Open questions** in the summary file — never guess, never merge people.
4. Commit per the AGENTS.md format with the `[auto]` prefix, e.g. `[auto] transcript(<subject>): summary + 3 people updated`.
