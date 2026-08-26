# Workstream C — Work-Product Templates Spec
**Status:** Draft for ratification
**Governs:** the six files `/apply` writes to `applications/<company>/`, and the template files in `skills/career-application-engine/templates/`.

## 1. General rules

- Templates are versioned files in the repo; a change to a template is a commit, visible in history. Same template + same store data = same result (PRD consistency goal).
- Every generated document footer records: template version (git short hash), store entities used (IDs), brief used (path + date), model.
- Voice: all prose products draw from `context/voice.md` (Rules > Samples > Learned, in that priority). No em-dash rule violations, no corporate filler, nothing "AI-sounding" — the voice file is the arbiter.
- Only `confirmed` accomplishments may appear in any product (store spec §8.3).

## 2. The six products

### 1. Customized CV — `cv.md`
- **Source of truth:** the master achievement inventory (`store/positions.md` + `store/accomplishments.md`), *not* a prior CV file — every application re-derives from the store.
- **Variants by role family:** `ctro`, `cto-cdo`, `epmo`, `consulting-md`. The skill picks the family from the posting (announcing its choice); each family has a fixed section order and emphasis profile defined in `templates/cv-<family>.md`.
- Requirement keywords from the posting are mirrored where honest; never keyword-stuffed.
- Length: 2 pages equivalent; oldest roles compress to one line beyond 15 years.

### 2. Cover letter — `cover-letter.md`
- Structure: hook (company-specific insight from the brief) → bridge (why Charlie, citing 2–3 proof points by store ID) → close (specific, low-friction ask). ≤1 page, 3–5 paragraphs.
- Draws angles from `store/positioning-library.md` first; a new angle that works gets written back (`ang-` entity).
- The reflection-touchpoint answer (workflow step 5) must appear, woven in, not bolted on.

### 3. Relevant bio — `bio.md`
- Audience-appropriate: board-facing, exec-search, or ops-facing — chosen from the posting context, built on the per-audience intro summaries ingested at bootstrap.
- Two lengths in one file: 100-word and 250-word.

### 4. Company research sheet — `research-brief.md`
- A copy of (or pointer to) the Workstream B brief used, so the application folder is self-contained.

### 5. Network analysis — `network.md`
- Ranked contact plan from the brief's Network overlay section:
  - **Primary** (works there now) → ranked by relationship strength (boss/report > colleague > recruiter > connection-only).
  - **Secondary** (can introduce) → ranked by strength × closeness to the hiring org.
- **Reach-out threshold (default):** any primary contact with relationship ≥ colleague, or any secondary path to the hiring manager's org, triggers a "reach out before applying" recommendation at the top of the file.
- For each recommended contact: a drafted note in Charlie's voice (≤120 words), referencing real shared context from `people/` notes.

### 6. Screening-question responses — `screening.md`
- Anticipated questions for this posting, each answered from the bank (`store/screening-qa.md`) where a match exists, drafted fresh where not — and every fresh Q&A writes back to the bank (`sq-` entity).
- **Length standards:** short-answer fields ≤75 words; essay fields ≤250 words; yes/no with justification ≤40 words.
- **Compensation questions:** never answer with a number unless `memory/preferences.md` provides an approved range; otherwise draft the deflection pattern stored at `sq-comp-default`.
- **Location/relocation:** answered from `memory/preferences.md` constraints; never improvised.

## 3. Template files (in `skills/career-application-engine/templates/`)

`cv-ctro.md`, `cv-cto-cdo.md`, `cv-epmo.md`, `cv-consulting-md.md`, `cover-letter.md`, `bio.md`, `network.md`, `screening.md` — each containing the fixed structure with `{placeholders}`, plus a header comment: purpose, when it was last revised, and what store fields it consumes. Scaffold ships structural v1 stubs; they get tuned during Phase 6 dry runs (every manual correction is a template fix, not a one-off edit).

## 4. Voice & style guide (shared)

Lives in `context/voice.md`, not per-template, so every skill benefits:
- `## Rules` — hard lines (sentence length, banned phrases, formality bounds)
- `## Samples` — 3+ passages Charlie actually wrote (seeded at bootstrap from real cover letters in the archive)
- `## Learned` — append-only observations from edits (writer-voice skill owns this section)
