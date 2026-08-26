# Automation — background jobs

Headless runs of designated skills via `claude -p`, scheduled by the OS. **One designated scheduler machine only** (see `specs/engineering-conventions.md` §5) — other machines run skills interactively.

## The jobs

| Job | Default schedule | Model | What it does |
|---|---|---|---|
| `transcript-sweep` | hourly, 7am–9pm | mid | Processes new files in `inbox/transcripts/` |
| `application-pulse` | daily, 8am | cheap | Checks active applications' postings are still live |
| `store-hygiene` | nightly, 2am | cheap | Validates store conventions; fixes mechanical, flags judgment |
| `weekly-digest` | Sunday, 6pm | mid | The passive-review digest → `automation/digests/` |

## Setup (macOS, launchd)

```bash
chmod +x automation/run-job.sh
# Test each job once by hand first:
./automation/run-job.sh store-hygiene
cat _cache/logs/store-hygiene-$(date +%Y-%m-%d).log

# Then install the schedules:
cp automation/launchd/*.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.life-os.*.plist
launchctl list | grep life-os   # verify
```

Before copying, edit each plist's `WorkingDirectory` and program path to your clone's absolute path.

## Setup (Linux, cron)

```cron
0 7-21 * * *  /path/to/life-os/automation/run-job.sh transcript-sweep
0 8    * * *  /path/to/life-os/automation/run-job.sh application-pulse
0 2    * * *  /path/to/life-os/automation/run-job.sh store-hygiene
0 18   * * 0  /path/to/life-os/automation/run-job.sh weekly-digest
```

## Behavior guarantees

- Every run: `git pull --rebase` first; a failed rebase aborts the run (never auto-resolved).
- All commits prefixed `[auto]`; the weekly digest lists them for passive audit.
- Failed pushes are retried with backoff and otherwise left for the next run.
- Logs: `_cache/logs/<job>-<date>.log`, 30-day retention, gitignored.
- Model routing lives in one place (`run-job.sh`); override with `LIFEOS_MODEL_CHEAP` / `LIFEOS_MODEL_MID`.

## Notes

- `run-job.sh` uses `--dangerously-skip-permissions` because headless runs cannot answer permission prompts. The jobs are constrained by their prompt files and the compose contract; review `automation/jobs/*.md` before scheduling.
- `/apply` is never scheduled — it has mandatory human touchpoints.
