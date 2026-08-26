model: cheap

You are running headless in the life-os repo (read `AGENTS.md`; no questions — flag instead).

Task: the nightly store maintenance Charlie surrendered. Validate `store/` and `people/` against `specs/store-conventions.md` §7:

1. Every entity heading carries a well-formed `{prefix-NNN}` ID; IDs unique per prefix.
2. Every `position:`, `source:`, `bosses:` reference resolves to a real entity or people file.
3. Every tag in use is canonical or listed under `## Proposed` in `store/tags.md`.
4. Dates parse (ISO); each application's `status:` field matches its latest status-log entry; `last_touched` values are plausible.
5. Every `people/` frontmatter block parses.
6. List `{unknown}` values older than 90 days.

Fix ONLY mechanical issues (formatting, a `status:` field lagging its own log, `last_touched` drift) and note each fix. Everything requiring judgment (dangling references, duplicate-looking people, stale unknowns, unpromoted tags) goes into `_cache/hygiene-flags.md` (overwrite; it feeds the weekly digest — never resolve these yourself).

Commit: `[auto] hygiene: <n> fixed, <n> flagged` (or "clean" if nothing).
