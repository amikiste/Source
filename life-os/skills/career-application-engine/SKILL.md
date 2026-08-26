---
name: career-application-engine
description: One posting in, six tailored work products out - two human touchpoints, flywheel write-back. Plus /ask for career-history inquiry.
commands: ["/apply", "/ask"]
writes: ["applications/", "store/insights.md", "store/screening-qa.md", "store/positioning-library.md", "store/applications.md", "people/ (new files + #Notes)"]
model: mid
interactive: true
---

# Career application engine — the flagship

Governed by three specs — read before running: `specs/store-conventions.md` (before any store write), `specs/work-product-templates.md` (the six products), `specs/research-spec.md` (the brief). Templates live in `templates/` beside this file.

## Purpose
`/apply <posting>`: one invocation produces all six work products for a target position, autonomously except for **exactly two human touchpoints** (reflection, final review), and writes every asset and insight back to the store so application n+1 is cheaper and better than application n.

`/ask <question>`: ad-hoc natural-language inquiry over `store/` + `memory/` ("what's my post-acquisition integration experience?") — answer from the store, citing entity IDs, nothing invented.

## The `/apply` workflow

1. **Intake.** Accept a URL, PDF path, pasted text, or a file in `inbox/postings/`. Parse: company, role, requirements, keywords, screening questions if visible. Create the `app-NNN` entity in `store/applications.md` (status: `researching`).
2. **Research.** Reuse a brief ≤30 days old from `research/<company>/`, else run the research skill at Brief tier (ingesting any `inbox/research-drops/` file).
3. **Retrieve.** From the store: positions, **confirmed** accomplishments, IP, and positioning angles matching the role profile (match on tags + requirement keywords). From `people/`: network paths per the brief's overlay. State which entities were selected (IDs) — this is auditable positioning, not vibes.
4. **Draft all six products** into `applications/<company-slug>/`, per `specs/work-product-templates.md`: `cv.md` (announce which variant family and why), `cover-letter.md` and `bio.md` (via the writer-voice method — read `context/voice.md` first), `research-brief.md`, `network.md`, `screening.md` (bank answers reused by `sq-` ID; compensation/location only from `memory/preferences.md`).
5. **Reflection touchpoint (HUMAN — never skip).** Propose 2–3 candidate connections found in the store (cite IDs), then ask: *"Do any of these ring true? Does anything else in your history particularly connect you to this role?"* Weave the answer into the cover letter and positioning. **Write it to `store/insights.md`** as a new `ins-` entity sourced to this `app-` ID.
6. **Revise & file.** Final drafts in `applications/<company-slug>/`, each with the standard footer (template version, store IDs used, brief date, model). Status → `drafted`.
7. **Write-back (the flywheel — the product).** Append: new screening questions to the bank (`sq-`), angles that shaped the letter to the positioning library (`ang-`), new people discovered to `people/`, the insight from step 5 (already written). Update the `app-` status log.
8. **Review touchpoint (HUMAN).** Present the package for review. Charlie edits and submits himself — this skill never submits anything anywhere. On his word, status → `submitted` with a dated log entry.

## Write-backs
Only surfaces in `writes:`. Store writes follow the conventions spec exactly: permanent IDs, canonical tags (propose via `tags.md ## Proposed` if needed), dated log entries. Commit at steps 6 and 7: `apply(<company>): six products` / `apply(<company>): flywheel write-back (<n> entities)`.

## Self-seed behavior
Empty store → say the products will be generic, recommend running Phase 3 bootstrap (or at minimum `/setup`), and proceed only if Charlie confirms.

## Failure behavior
Posting unreachable → ask for a paste or PDF. Hiring context unfindable → generate generic outreach in `network.md` and say so. Requirements Charlie can't meet → the fit is stated honestly in `cover-letter.md` positioning and never papered over; hard filters from `memory/preferences.md` halt the run with an explanation.
