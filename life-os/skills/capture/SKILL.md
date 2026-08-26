---
name: capture
description: Front-door router - files a thought, task, link, or name where it belongs.
commands: ["/capture"]
writes: ["memory/journal/", "context/projects.md", "people/ (new files + frontmatter)", "store/tags.md#Proposed"]
model: cheap
interactive: false
---

# Capture — file anything

## Purpose
Zero-friction intake. Charlie throws anything at it — a thought, a task, a link, a person's name, an observation — and it lands in the right place, dated. The router, not a thinker: classify, file, confirm in one line.

## Inputs
Free text (or a link, or a name) as `$ARGUMENTS` or the next message.

## Steps
1. **Classify** the item (may be multiple):
   - *Person* — a name, possibly with context ("met Raj at the CIO dinner, runs data at Vantage").
   - *Project item* — task or update belonging to a heading in `context/projects.md`.
   - *Thought/observation* — everything else, including links worth keeping.
2. **File:**
   - Person → match against `people/` per `specs/store-conventions.md` §6 (slug → name → alias; ambiguity: ask). New person → new file from the template in `people/README.md` with `source: capture`; known person → append a dated line under `## Notes`, update `last_touched`.
   - Project item → append a dated bullet under the existing project heading. No matching heading → ask whether to create one (interactive) or file to journal with a `project?` marker (headless).
   - Thought → append to `memory/journal/YYYY-MM-DD.md` (create the day file if needed), one dated bullet, link included.
3. **Confirm** in one line: what was filed, where. No essays.

## Write-backs
Only the surfaces in `writes:`. Everything appended, everything dated. Commit: `capture: <one-line summary>`.

## Self-seed behavior
Missing `memory/journal/` or `people/` → create them (with the README template) and proceed.

## Failure behavior
Unclassifiable → journal, with the raw text preserved verbatim and a `triage?` marker. Never drop an item; never guess a person merge.
