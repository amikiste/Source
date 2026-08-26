---
name: setup
description: Onboarding interview that seeds context/ and memory/. Re-runnable to update.
commands: ["/setup"]
writes: ["context/you.md", "context/voice.md", "context/projects.md", "memory/background.md", "memory/preferences.md"]
model: mid
interactive: true
---

# Setup — onboarding interview

## Purpose
Seed (or refresh) Charlie's shared memory through a short layered interview, so every other skill starts personalized. Never overwhelm: start with what can be extracted automatically, ask only for what's missing.

## Inputs
- Optional: a CV file path (PDF or markdown), anywhere Charlie points to.
- Charlie's answers.

## Steps
1. **Check state.** Read `context/` and `memory/`. If mostly filled, say so and ask what to update; only walk the full flow on placeholders (`{unknown}`, `{add ...}`).
2. **CV first.** Ask for a CV path. If provided, extract: name, current role, career history, quantified achievements, credentials. Show what was extracted and confirm before writing anything.
3. **Fill `context/you.md`** — name, role, company, one-two sentence "what you do", working style. Confirm.
4. **Fill `memory/background.md`** — narrative summary, career arc, credentials, outside-of-work (optional; accept "skip").
5. **Fill `memory/preferences.md`** — target roles, location constraints, compensation range *approved for screening answers* (explain why it's asked: it becomes the only permitted source for compensation questions), hard filters, communication preferences. Offer reasonable defaults; accept "decide later" → `{unknown}`.
6. **Seed `context/voice.md`** — ask for 2–3 real writing samples (a sent cover letter, a good email). Paste under `## Samples`. Ask for hard rules (banned phrases, tone bounds) under `## Rules`.
7. **Seed `context/projects.md`** — one heading per active project/campaign.
8. **Recap** what was written and where; remind that everything is editable by hand anytime.

## Write-backs
Only the files listed in `writes:`. Replace placeholders; never delete content a human added. Commit: `setup: seed memory (<what changed>)`.

## Self-seed behavior
This skill *is* the seeder. If folders are missing entirely, create them per `AGENTS.md`'s surface table before interviewing.

## Failure behavior
If the CV can't be read, fall back to asking questions section by section. Never write invented values — anything unanswered stays `{unknown}`.
