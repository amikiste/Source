# Workstream A — Store Conventions Spec
**Status:** Draft for Charlie's ratification (critical path for Phase 3 bootstrap)
**Governs:** everything under `store/`, plus `people/` file schemas and matching rules.

## 1. Principles

The store is agent-maintained markdown. No spreadsheet, no database. Referential integrity comes from three things: stable IDs, a controlled tag vocabulary, and the nightly `store-hygiene` job that validates these conventions. Humans may read or edit anything; they are never required to.

## 2. File-per-domain layout

| File | Contains | Entity prefix |
|---|---|---|
| `store/positions.md` | Every role held: primary work, volunteer, board, fractional | `pos-` |
| `store/accomplishments.md` | Achievement statements with quantified impact | `acc-` |
| `store/ip.md` | Patents, frameworks, methods created | `ip-` |
| `store/engagements.md` | Speaking, publications, panels | `eng-` |
| `store/applications.md` | Application pipeline with status logs | `app-` |
| `store/insights.md` | The flywheel: newly articulated self-knowledge | `ins-` |
| `store/screening-qa.md` | Screening-question bank with best-answer drafts | `sq-` |
| `store/positioning-library.md` | Reusable angles, phrasings, fragments that worked | `ang-` |
| `store/tags.md` | The controlled tag vocabulary (see §5) | — |

## 3. Entity format

One `##` section per entity. The heading carries a human-readable title and the stable ID in braces. Structured fields are a bullet block directly under the heading; free text follows. Example (positions):

```markdown
## CTrO, Example Corp {pos-007}
- org: Example Corp
- title: Chief Transformation Officer
- start: 2019-03
- end: 2022-06
- type: primary            # primary | volunteer | board | fractional
- bosses: [jane-doe]       # people/ file slugs
- tags: [post-acquisition-integration, epmo]

Free-text narrative, context, and notes go here.
```

Cross-domain example (accomplishments):

```markdown
## Consolidated three PMOs into one ePMO {acc-041}
- position: pos-007
- impact: $12M annual run-rate savings; 40% cycle-time reduction
- tags: [epmo, workforce-transition]
- confirmed: 2026-09-01    # date Charlie ratified the statement

STAR-format detail if available.
```

**Rules**
1. **IDs are permanent.** Assigned by the agent at creation, sequential per prefix, never reused, never renumbered — even if an entity is retired (mark `- retired: <date>` instead of deleting).
2. **`position:` is the spine.** Accomplishments, IP, and (where relevant) insights reference a `pos-` ID. An entity with no position link uses `position: none` explicitly.
3. **Dates** are ISO: `YYYY-MM-DD`, or `YYYY-MM` where the day is unknown. Never invent precision.
4. **Unknown values** get `{unknown}` — visible, greppable, never guessed (compose contract rule 5).
5. **Field keys are lowercase, fixed per domain.** New keys require a spec change, not an ad-hoc addition.

## 4. Append-only logs

`insights.md` and per-application status entries are chronological logs. New entries append at the end with a date and a source:

```markdown
## Nonprofit CxO tenure connects to mission-driven roles {ins-012}
- date: 2026-09-14
- source: app-003          # the application cycle that surfaced it
- tags: [positioning]

DSG application: recent nonprofit CxO tenure is a direct bridge to nonprofit-sector roles...
```

Application status is a log *inside* the application entity:

```markdown
## VP Transformation, Acme Health {app-003}
- company: acme-health
- role: VP Transformation
- posting: https://... (or inbox/postings/acme-health.pdf)
- opportunity_type: formal   # formal | networking
- status: interviewing       # researching | drafted | submitted | interviewing | closed-won | closed-lost | withdrawn

### Status log
- 2026-09-10: submitted via Workday portal
- 2026-09-18: recruiter screen scheduled (see people/sam-recruiter.md)
```

The `status:` field always reflects the latest log entry; hygiene checks the two agree.

## 5. Controlled tag vocabulary

`store/tags.md` is the single list of allowed tags (kebab-case), grouped by category (transformation themes, functional domains, industries, positioning). Skills may **propose** a new tag by adding it under a `## Proposed` heading with one usage; promotion into the canonical list happens in the weekly digest review. Hygiene flags any tag in use that is neither canonical nor proposed.

Seed categories (bootstrap fills these from the CV and archive): post-acquisition-integration, agile-transformation, epmo, workforce-transition, ai-adoption, turnaround, nonprofit, board-governance — extended during Phase 3, then frozen to the promotion process.

## 6. `people/` schema and matching

One file per person: `people/<kebab-full-name>.md`. YAML frontmatter for structure, markdown body for history:

```markdown
---
name: Jane Doe
aliases: [Janey D]
company: Acme Health
role: Chief People Officer
relationship: colleague      # colleague | boss | report | client | recruiter | prospect | friend | family
context_met: ePMO consolidation project, 2020
last_touched: 2026-09-18
source: linkedin-export      # linkedin-export | transcript | application | manual | capture
---

# Jane Doe

## Notes
<!-- skills append dated notes below; never edit above this line except frontmatter fields -->
- 2026-09-18 (transcript): Discussed VP Transformation role; she offered intro to CTO.
```

**Matching rules (in order):** exact slug match → case-insensitive name match → alias match → if ambiguous (two Jane Does), ask when interactive / flag in digest when headless — never merge automatically. New person → new file, with `source:` recorded. `last_touched` is updated by any skill that appends a note.

**Sensitivity:** `people/` is the most sensitive data in the repo. It never leaves the repo; no skill quotes it into web queries (search "Jane Doe Acme" is fine; pasting note contents into a search is not).

## 7. Hygiene validation rules (nightly job)

1. Every entity has a well-formed heading `{prefix-NNN}`; IDs unique per prefix.
2. Every `position:` / `source:` / `bosses:` reference resolves.
3. Every tag is canonical or proposed.
4. Dates parse; `status:` matches last status-log entry; `last_touched` ≤ today.
5. No `{unknown}` older than 90 days without a digest flag.
6. Frontmatter parses in every `people/` file.

Mechanical fixes (formatting, `last_touched` drift) are corrected and committed; judgment calls are flagged in the weekly digest, never auto-resolved.

## 8. Bootstrap decisions (defaults for ratification)

1. **Archive scope:** mine all ~115 OneDrive folders in one pass; text-first. Folders that are image/PDF-heavy (contact screenshots, scanned postings) get a stub application entity with `- bootstrap: needs-manual-pass` and are listed for one batch review.
2. **LinkedIn:** re-export before seeding (current extract is Oct 2024); the CSV lands in `inbox/` and seeds `people/` frontmatter only (name, company, connected-on) — no fabricated relationship or context fields.
3. **Accomplishment vetting:** bootstrap marks every mined accomplishment `- confirmed: {unknown}`; Charlie's single review pass confirms or vetoes; unconfirmed entities are excluded from work products.
4. **Applications history:** one `app-` entity per archive folder, status `closed-lost` unless evidence says otherwise; outcomes backfilled opportunistically, not exhaustively.
