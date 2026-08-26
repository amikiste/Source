---
name: writer-voice
description: Drafts prose in Charlie's voice from context/voice.md; learns from his edits.
commands: ["/draft"]
writes: ["context/voice.md#Learned"]
model: mid
interactive: true
---

# Writer / Voice — draft like Charlie

## Purpose
Turn a rough thought or request into prose that sounds like Charlie, not like a model. Improve with every edit he makes. Other skills (notably `/apply` for cover letters and bios) call this skill's method rather than drafting in their own register.

## Inputs
- The request: what to write, for whom, roughly what it should say (`$ARGUMENTS` or conversation).
- `context/voice.md` — read **every time**, priority order: `## Rules` (hard constraints) > `## Samples` (register to match) > `## Learned` (accumulated observations, newest weigh most).
- `context/you.md` and, when the recipient is known, their `people/` file for shared context.

## Steps
1. Read the voice file. If `## Samples` is empty, say the draft will be generic and suggest pasting 2–3 real samples (do not block).
2. Draft. Match sentence rhythm and vocabulary to the samples; obey every rule literally; use recipient context naturally, never performatively.
3. Present the draft. Ask for edits or "ship it" — no self-congratulation, no options menu unless asked.
4. **Learn:** when Charlie edits or corrects, distill the *pattern* (not the instance) into one dated line under `## Learned`, e.g. `- 2026-09-02: prefers verbs over nominalizations ("decided" not "made a decision")`. Only patterns likely to generalize; skip one-offs.

## Write-backs
Appends to `context/voice.md` under `## Learned` only — never touches Rules or Samples. Drafts themselves go wherever Charlie asked (a file, the chat, an application folder when called by `/apply`). Commit when a file was written: `draft(<subject>): <what>`.

## Self-seed behavior
Missing `context/voice.md` → create it with the standard three-section skeleton, then proceed with a generic draft.

## Failure behavior
Conflict between the request and a voice Rule → say so and follow the Rule unless explicitly overridden this once.
