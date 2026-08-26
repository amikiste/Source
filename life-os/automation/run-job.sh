#!/usr/bin/env bash
# Generic headless job runner: ./automation/run-job.sh <job-name>
# Jobs are prompt files in automation/jobs/<job-name>.md, executed via `claude -p`.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JOB="${1:?usage: run-job.sh <job-name>}"
JOB_FILE="$REPO/automation/jobs/$JOB.md"
[ -f "$JOB_FILE" ] || { echo "unknown job: $JOB" >&2; exit 1; }

LOG_DIR="$REPO/_cache/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$JOB-$(date +%Y-%m-%d).log"

# Model routing (specs/engineering-conventions.md §4). Override via env if model
# names change; this is the single place class -> model is mapped.
MODEL_CHEAP="${LIFEOS_MODEL_CHEAP:-haiku}"
MODEL_MID="${LIFEOS_MODEL_MID:-sonnet}"
CLASS="$(grep -m1 '^model:' "$JOB_FILE" | awk '{print $2}' || true)"
case "${CLASS:-cheap}" in
  mid) MODEL="$MODEL_MID" ;;
  *)   MODEL="$MODEL_CHEAP" ;;
esac

notify() { # macOS notification; silently no-op elsewhere
  command -v osascript >/dev/null 2>&1 && \
    osascript -e "display notification \"$2\" with title \"life-os: $1\"" || true
}

cd "$REPO"
{
  echo "=== $JOB @ $(date -u +%FT%TZ) model=$MODEL ==="

  # Sync first; a failed rebase aborts the run (never auto-resolve).
  if ! git pull --rebase --autostash; then
    git rebase --abort 2>/dev/null || true
    echo "PULL/REBASE FAILED - aborting run"
    notify "$JOB" "sync failed; run skipped"
    exit 1
  fi

  claude -p "$(cat "$JOB_FILE")" --model "$MODEL" --dangerously-skip-permissions || {
    echo "JOB FAILED"
    notify "$JOB" "job failed; see log"
    exit 1
  }

  # Commit anything the job wrote but didn't commit itself.
  if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "[auto] $JOB: run $(date +%Y-%m-%d)" || true
  fi

  # Push with backoff; a failed push is not fatal (next run pushes).
  for delay in 0 4 8 16 32; do
    sleep "$delay"
    git push && break || echo "push retry in ${delay}s..."
  done

  # 30-day log retention
  find "$LOG_DIR" -name '*.log' -mtime +30 -delete 2>/dev/null || true
  echo "=== done @ $(date -u +%FT%TZ) ==="
} >>"$LOG" 2>&1
