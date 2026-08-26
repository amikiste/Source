model: cheap

You are running headless in the life-os repo (read `AGENTS.md`; no questions — flag instead).

Task: pulse-check the active application pipeline. This is NOT job discovery — only positions already in `store/applications.md`.

1. Collect every application entity with `status: submitted` or `status: interviewing` that has a posting URL.
2. Fetch each URL. Classify: live / changed / gone / unreachable.
3. For **gone** postings: append a dated line to that application's `### Status log` — "posting removed (signal: role filled or pulled; consider follow-up)". Do not change the `status:` field; that is Charlie's call.
4. For **unreachable** (network error, not 404): note it in the log file only; retry next run.
5. Write nothing else. Commit: `[auto] pulse: <n> checked, <n> flagged`.
6. If anything was flagged, end your output with the single line `NOTIFY: <n> posting(s) disappeared` so the wrapper surfaces it.
