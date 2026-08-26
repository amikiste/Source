# Product Requirements Document: Personal AI Skills Suite
**Owner:** Charlie Fleet
**Date:** August 26, 2026
**Status:** Draft v2.0 — supersedes *Career Application Engine PRD v1.0* (Aug 4, 2026) by generalizing it into a multi-skill suite
**Lineage:** Reconciles three inputs: (1) the Career Application Engine PRD v1.0, (2) the compose-contract architecture of [remix-yourself-starter](https://github.com/remixrevco/remix-yourself-starter/), and (3) the mature single-skill patterns of [job-sniper](https://github.com/jugbandman/job-sniper) (setup interview, depth tiers, headless background runs, model routing).

---

## 1. Background

Two design efforts converged here.

The first (PRD v1.0) solved a specific problem: reduce the transaction cost of the n-th online job application to near zero while capturing every asset and insight back into a compounding knowledge base. Its architecture: a private GitHub repo as system of record, Claude Code as orchestrator, a relational career data store, and an `/apply` workflow with exactly two human touchpoints.

The second is a broader observation: the same person needs a *suite* of AI skills throughout the day — drafting in his own voice, processing meeting transcripts, researching companies and people, capturing stray thoughts — and all of them need the same thing the application engine needs: durable knowledge of who he is, held in a central location he controls, **not** in any AI provider's memory feature.

The remix-yourself-starter demonstrates the architecture that makes a suite work: skills as plain-markdown prompts, memory as plain files in shared folders, and a small filesystem contract ("the compose contract") that lets independently built skills share one memory with zero glue code. Job-sniper demonstrates what one skill looks like fully built out: onboarding interview, config-driven personalization, tiered research depth, deterministic helpers where reproducibility matters, and scheduled background runs via headless `claude -p`.

This PRD merges all three. The Career Application Engine becomes the flagship skill inside a suite; the suite adopts the compose contract as its foundation and extends it.

## 2. Problem Statement (Ratified)

> Build a single private repository that (a) holds Charlie's background, memories, voice, people, and career history as plain, human-editable, provider-independent files; (b) hosts a growing suite of skills — each useful alone, all compounding through shared memory — invocable from Claude Code **or any other capable AI agent**; (c) runs designated skills unattended in the background on a schedule; and (d) preserves the v1.0 flywheel: every skill run writes its assets and insights back to the store, so the system is better after every use.

## 3. Goals and Non-Goals

**Goals**
1. **Provider-independent memory.** All personal context lives as plain files (markdown + CSV) in the repo. No skill may depend on provider-side memory. Switching AI providers loses nothing.
2. **Multi-runtime invocation.** Every skill is a provider-neutral prompt file; thin adapters expose it to Claude Code (slash commands), and an `AGENTS.md` entry point makes the repo legible to any other agent (Cursor, Codex CLI, Gemini CLI, etc.).
3. **Composability.** Skills follow the compose contract: read shared memory freely, write narrowly to owned surfaces, append never clobber, self-seed if missing. New skills join by following the contract; nothing is wired by hand.
4. **Background operation.** Designated skills run unattended on a schedule (cron/launchd + headless `claude -p`). Platform lock-in for the *scheduler* is acceptable; the skills themselves stay portable.
5. **The flywheel (carried from v1.0).** Every application cycle writes insights, screening questions, people, and positioning angles back to the store. Every transcript enriches `people/`. Every edited draft teaches the voice file.
6. **One invocation → six work products** for a target position (`/apply`), with exactly two human touchpoints (carried unchanged from v1.0 §7).
7. **Standalone deep research** (`/research`), usable with or without an application, comparable across companies and time.
8. **Ad-hoc natural-language inquiry** of career history and personal memory from any endpoint — trivially satisfied because everything is plain files any agent can read.
9. **Multi-machine operation** via GitHub; phone-initiated runs desirable, not mandatory.

**Non-Goals (deliberate exclusions)**
- Job discovery/matching. Charlie selects which positions enter the pipeline. (Job-sniper's alert-scanner/watchlist subsystem is explicitly *not* adopted, though its background-run mechanics are.)
- Automated submission to job boards. The engine prepares; Charlie submits.
- Relationship management or outreach automation. Networking remains human-led.
- Daily planning ("today-planning" from remix-yourself-starter). Deferred; the architecture accepts it later without change if wanted.
- Multi-tenant, sharing, or permissions. Single user.

## 4. Users

Single user: Charlie. Privacy posture: private repository; contact data never leaves owned surfaces; secrets in `.env` (gitignored), never in prompts or committed files.

## 5. System Architecture (Converged)

| Layer | Choice | Rationale |
|---|---|---|
| System of record | Private GitHub repository | Cloud, multi-endpoint, versioned; kills asset leakage structurally (v1.0, unchanged) |
| Memory model | Compose contract v1.1: `context/` + `people/` + `memory/`, plain markdown | Provider-independent, human-editable, git-diffable; proven cross-skill sharing model (remix) |
| Career data store | `store/*.csv` — one CSV per table, cross-keyed; optional generated `career.xlsx` view | **Changed from v1.0** (xlsx canonical → CSV canonical); see §9 rationale |
| Skills | `skills/<name>/SKILL.md` — provider-neutral markdown prompts | The prompt is the product (job-sniper); readable, editable, forkable |
| Primary orchestrator | Claude Code, via `.claude/commands/` adapters | Strongest tool for long autonomous file work (v1.0, unchanged) |
| Other-agent entry | `AGENTS.md` at repo root + `CLAUDE.md` pointing to it | Emerging cross-provider convention; any agent opening the repo learns the contract and skill index |
| Background runs | cron (Linux) / launchd (macOS) → shell wrapper → `claude -p` headless, cheap model | Job-sniper's proven pattern; scheduler platform lock-in accepted by design |
| Historical corpus | OneDrive Applications archive, read in place | One-time mining pass; archive stays frozen (v1.0, unchanged) |
| Research amplifier | Gemini Deep Research output dropped into `inbox/` as a source | Agent synthesizes and cross-examines rather than trusting one source (v1.0, unchanged) |
| Deterministic helpers | Optional small scripts (e.g., CSV validation, xlsx generation) | Code only where LLM judgment is a liability (job-sniper's scoring-engine lesson) |

**Eliminated alternatives (cumulative record).** From v1.0: claude.ai Project as engine; Airtable/Notion as KB; custom API pipeline / n8n; federated multi-tool per artifact. Newly eliminated here: **xlsx as canonical store** (binary format is hostile to non-Claude agents and to git merges; see §9); **vector-database/RAG memory** (the prior Swarm/LlamaIndex prototype's approach — opaque, rebuild-to-update, embedding-provider-dependent; plain markdown is the requirement, and RAG can be layered on later *over* the files if the corpus outgrows a context window); **provider memory features** (violates Goal 1 by definition).

### 5.1 Repository Layout

```
<repo>/
├── AGENTS.md                  # entry point for ANY agent: what this repo is, the contract, skill index
├── CLAUDE.md                  # Claude Code operating instructions (points at AGENTS.md, adds specifics)
├── README.md
├── .compose-contract          # contract version marker (v1.1)
├── .env / .env.template       # secrets (gitignored) / documented template
│
├── context/                   # ── shared memory: compose contract v1 (adopted as-is) ──
│   ├── you.md                 # identity, role, working style
│   ├── voice.md               # writing rules, samples, ## Learned (appended by writer skill)
│   └── projects.md            # active projects and campaigns
├── people/                    # one markdown file per person; ## Notes appended, never clobbered
│   └── <kebab-name>.md
├── memory/                    # ── contract extension (new in v1.1) ──
│   ├── background.md          # biography, career narrative, credentials
│   ├── preferences.md         # durable preferences and constraints
│   └── journal/               # dated append-only entries (from /capture and reflections)
│
├── store/                     # ── career data store: CSV canonical ──
│   ├── positions.csv          # org, title, dates, type, boss(es), position_id
│   ├── accomplishments.csv    # statement, quantified impact, position_id, theme tags
│   ├── ip.csv                 # patents, frameworks, methods; position_id
│   ├── people-index.csv       # structured index over people/ (see §9.2)
│   ├── engagements.csv        # speaking, publications, panels
│   ├── applications.csv       # company, role, date, opportunity_type, status/outcome
│   ├── insights.csv           # the flywheel table
│   ├── screening-qa.csv       # question bank with best-answer drafts
│   ├── positioning-library.csv# reusable angles, phrasings, fragments that worked
│   └── career.xlsx            # OPTIONAL generated multi-tab view (never hand-edit; regenerated)
│
├── skills/                    # ── the suite: one folder per skill, provider-neutral ──
│   ├── setup/SKILL.md
│   ├── capture/SKILL.md
│   ├── writer-voice/SKILL.md
│   ├── transcription-intake/SKILL.md
│   ├── research/SKILL.md
│   └── career-application-engine/
│       ├── SKILL.md
│       └── templates/         # six work-product templates (versioned; changes visible in git)
│
├── .claude/commands/          # thin adapters: /setup /capture /draft /process-transcript
│                              #                /research /apply /ask  → each reads its SKILL.md
│
├── applications/<company>/    # /apply outputs: the six work products per target position
├── research/<company>/        # /research briefs (standalone or application-linked)
├── inbox/                     # drop zone: transcripts, postings (PDF/URL notes), Gemini DR outputs
├── automation/                # cron/launchd definitions + shell wrappers + headless job prompts
└── _cache/                    # run logs, dedup state (gitignored)
```

### 5.2 The Compose Contract, v1.1

Adopted from remix-yourself-starter v1 and extended. Every skill — current and future — agrees to:

1. **Read freely.** Any skill may read anything in `context/`, `people/`, `memory/`, and `store/` to personalize its output.
2. **Write narrowly.** Each skill writes only to surfaces it owns:
   - *writer-voice* appends to `context/voice.md` under `## Learned` only.
   - *transcription-intake* and *research* append to `people/<name>.md` under `## Notes`, create new `people/` files, and update `store/people-index.csv`.
   - *capture* appends to `memory/journal/`, `context/projects.md` (under existing headings), and creates `people/` files.
   - *career-application-engine* owns `applications/`, and appends rows to `store/` tables (insights, screening-qa, positioning-library, applications, accomplishments-on-confirmation).
   - *research* owns `research/`.
3. **Append, never clobber.** Writes to shared files are additive and dated. Human-authored content is sacred. CSV writes append rows or fill empty cells; row deletion and schema changes require explicit human instruction.
4. **Self-seed if missing.** Any skill run in a fresh clone creates the minimal stubs it needs. Never fail because memory is absent.
5. **Stub, don't assume.** Unknown values get a visible placeholder (`{add role}`), never an invented one.
6. **Commit with readable messages.** Every skill run that changes files ends with `git add` + commit (+ push when a remote is reachable). Background jobs pull before running.

The `.compose-contract` marker records `contract: v1.1`. Remix-built or third-party v1 components remain compatible (they simply ignore `memory/` and `store/`).

## 6. The Skill Suite (v1 Roster)

| Skill | Commands | Origin | What it does |
|---|---|---|---|
| **setup** | `/setup` | job-sniper `setup.md`, generalized | One-time onboarding interview. Reads the CV; asks layered questions; seeds `context/`, `memory/`, and store stubs. Re-runnable to update. |
| **capture** | `/capture` | remix claude-skills-starter | Front-door router. Throw a thought, task, link, or name at it; it files to `memory/journal/`, `context/projects.md`, or `people/`. |
| **writer-voice** | `/draft` | remix writer-voice | Drafts emails/letters/posts in Charlie's voice from `context/voice.md` (Rules + Samples + Learned); appends observations after edits. Used *by* the application engine for cover letters and bios. |
| **transcription-intake** | `/process-transcript` | remix transcription-intake | Transcript in (any tool, via `inbox/`); summary + decisions + action items out, filed onto the people involved. Also runs headless (§8). |
| **research** | `/research <topic\|company> [--brief]` | Merge of v1.0 §8 + remix researcher-meeting-prep + job-sniper depth tiers | **Quick tier** (default): tight, sourced answer to any question about a company, person, or topic; grounded in `people/` and `memory/` first, web second. **Brief tier** (`--brief`): the full fixed-template company research sheet from v1.0 §8 — business model, ownership/financials, leadership, strategy, tech/AI posture, culture, competition, risks, network overlay (via `people/` + people-index), and "angles" hooking company needs to Charlie's proof points. Ingests Gemini Deep Research files from `inbox/` as amplifying sources. Also covers meeting prep: `/research` on a person + upcoming meeting produces a pre-call brief from their `people/` history plus live web. |
| **career-application-engine** | `/apply <posting>`, `/ask <question>` | PRD v1.0 §6–7, intact | The flagship. Full workflow in §7. `/ask` is the ad-hoc career-history inquiry (Goal 8) over `store/` + `memory/`. |

Deliberately excluded from v1: today-planning (user decision), job discovery/alert scanning (non-goal).

**Adding skill n+1:** create `skills/<name>/SKILL.md` obeying §5.2, add a command adapter, add a row to `AGENTS.md`'s index. Nothing else. This is the whole extension model.

## 7. The `/apply` Workflow (carried from v1.0, adapted to suite)

1. **Intake** — Charlie supplies posting (URL, PDF, or text; or drops it in `inbox/`). Agent parses role, requirements, keywords.
2. **Research** — invokes the *research* skill at Brief tier (or ingests an existing brief from `research/<company>/`, including Gemini output if present).
3. **Retrieve** — queries `store/*.csv` for relevant positions, accomplishments, IP, and prior assets; queries `people/` + `people-index.csv` for network paths.
4. **Draft** — generates all six work products, using the *writer-voice* skill's voice file for the cover letter and bio:
   1. Customized CV, 2. Cover letter, 3. Relevant bio, 4. Company research sheet, 5. Network analysis, 6. Screening-question responses (seeded from `store/screening-qa.csv`).
5. **Reflection touchpoint (human)** — agent pauses: *"Does anything in your history particularly connect you to this role?"* Answer is incorporated into drafts **and** written to `store/insights.csv`.
6. **Revise & file** — final drafts written to `applications/<company>/`, committed.
7. **Write-back (the flywheel)** — append rows: insights, screening questions encountered, new people (file + index row), positioning angles used. Committed with a readable message.
8. **Review touchpoint (human)** — Charlie reviews, edits, submits himself.

Human touchpoints remain exactly two (steps 5 and 8). Because step 5 requires interactivity, `/apply` is an attended skill; it is not scheduled in the background.

## 8. Background Operation

**Mechanism (job-sniper pattern, platform lock-in accepted):** the OS scheduler (launchd on macOS, cron on Linux) fires a shell wrapper in `automation/`. The wrapper: `git pull` → run `claude -p "$(cat automation/jobs/<job>.md)"` headless on a cheap/fast model → `git commit && git push` → log to `_cache/logs/`. Job prompts are provider-neutral markdown like every other skill; only the wrapper + scheduler definition are platform-specific. Failures log and notify (macOS notification / email); they never block interactive use.

**v1 scheduled jobs:**

| Job | Schedule (default) | What it does |
|---|---|---|
| **transcript-sweep** | hourly, waking hours | Processes any new files in `inbox/transcripts/` through the *transcription-intake* skill; files summaries and people notes. |
| **application-pulse** | daily | Revisits posting URLs for applications with status *submitted/interviewing* in `store/applications.csv`; flags vanished postings (a follow-up signal) and drafts a status note. No discovery — only positions already in the pipeline. |
| **store-hygiene** | nightly | Validates CSV schemas/keys (deterministic script), regenerates `store/career.xlsx` view, reconciles `people-index.csv` against `people/`, commits. |
| **weekly-digest** | Sunday evening | Summarizes the week's flywheel: new insights, new people, application status changes, voice learnings → one markdown digest + notification. Replaces "keep the store updated" with "read what accumulated." |

**Model routing (job-sniper's lesson):** background jobs and parsing run on the cheapest adequate model (Haiku-class); interactive research/drafting on a mid-tier model (Sonnet-class); Deep briefs for top-priority targets may use a top-tier model. Routing is a per-job/per-skill setting in the skill file, editable like everything else.

## 9. Data Store Design (the one material change from v1.0)

### 9.1 CSV canonical, xlsx generated

v1.0 chose `career.xlsx` as canonical with agent-exported CSVs for diffability. This PRD inverts that: **the CSVs are canonical; the workbook is a generated, read-only convenience view.**

Rationale, driven by the new multi-runtime requirement:
- **Any agent can read/write CSV with plain file tools.** xlsx requires a library and invites silent corruption from non-Claude agents (Goal 2 would otherwise quietly re-lock the system to one runtime).
- **Git-native.** CSV diffs and merges work; binary xlsx conflicts are unrecoverable (v1.0 open question #17 dissolves).
- **Co-ownership is preserved.** Excel opens and edits a CSV directly — the "open in native Excel and edit at will" requirement survives; only multi-tab browsing moves to the generated workbook. The nightly *store-hygiene* job regenerates `career.xlsx` so a fresh browsable view always exists.
- Cross-keying (position_id as spine), table set, and seed sources are unchanged from v1.0 §9.

*Preserved alternative:* if editing CSVs in Excel proves unacceptable in practice, revert to xlsx-canonical with per-commit CSV export (v1.0 design) — the table schemas are identical either way, so the switch is mechanical.

### 9.2 People: markdown canonical, CSV index

v1.0's People *table* and the compose contract's `people/` *folder* merge:
- `people/<name>.md` is the canonical record — relationship, context, and the append-only `## Notes` history that transcripts, research, and applications feed.
- `store/people-index.csv` is an agent-maintained structured index (name, file path, company, relationship, source, last-touched) so the career engine's network analysis can scan structurally without opening every file. The *store-hygiene* job keeps it consistent.
- The LinkedIn export CSV seeds the index at bootstrap and remains a raw source in `inbox/`, refreshed quarterly.

## 10. Non-Functional Requirements

- **Co-ownership:** agent performs all routine maintenance; Charlie can open/edit/commit at will. One required habit: pull before editing (background jobs also pull before running).
- **Consistency:** work-product templates and skill prompts are versioned in the repo; template changes are visible in git history; same template + same data = same result.
- **Portability:** a skill must produce correct output when executed by any capable agent given only the repo contents. Provider-specific syntax lives only in adapter files (`.claude/`, wrappers).
- **Privacy:** private repo; People data treated as sensitive; secrets only in `.env`; background job logs contain no secrets.
- **Durability:** OneDrive archive untouched as legal-copy history; repo is the forward-looking system of record.
- **Degradation:** skills without web access fall back to memory-grounded answers and say so (remix researcher pattern).

## 11. Success Metrics (Draft)

- **Transaction time:** ≤30 minutes of Charlie's attention per application (two touchpoints + review) — carried from v1.0.
- **Flywheel health:** ≥1 new insight row and captured screening questions per application cycle; `people/` files grow with every transcript.
- **Consistency:** standardized inquiries produce stable outputs across runs and across runtimes.
- **Portability proof:** at least one skill run end-to-end from a non-Claude agent with correct output during pilot.
- **Background reliability:** scheduled jobs run ≥95% of scheduled slots over a month; zero corrupted-store incidents.
- **Adoption:** engine used for effectively all online applications after pilot; voice drafts preferred over from-scratch writing.

## 12. Outstanding Questions (Handoff List for Spec Workstreams)

**Workstream A — Data store spec** *(v1.0 items 1–5 carry over, plus:)*
1. Final CSV schemas: fields, keys, controlled vocabularies (theme tags), per table; quoting/encoding conventions for safe hand-editing.
2. `people-index.csv` field set and the sync rules against `people/` files.
3. Bootstrap scope: which of the ~115 archive folders to mine; handling image/PDF-heavy folders.
4. LinkedIn re-export before seeding.
5. Application status-history depth, and whether *application-pulse* may update status rows autonomously or only draft proposed changes.

**Workstream B — Research spec** *(v1.0 items 6–8 carry over, plus:)*
6. Final Brief-tier template sections and depth; Quick-tier output format.
7. Rules for recommending a Gemini Deep Research pass vs. agent-only research.
8. Source-quality and recency standards; conflict presentation.
9. Meeting-prep variant: trigger phrasing and brief format.

**Workstream C — Work-product templates** *(v1.0 items 9–12 carry over unchanged.)*

**Workstream D — Engineering/repo**
10. `AGENTS.md` and `CLAUDE.md` exact content; command-adapter wording; skill file frontmatter conventions.
11. Reflection-prompt design: open-ended vs. agent-proposed candidate connections (v1.0 item 14).
12. Multi-model quality loop as an optional pipeline step (v1.0 item 15); model routing table per skill (v1.0 item 16).
13. Scheduler targets: which machine(s) host cron/launchd; conflict policy if two machines schedule the same job; notification channel (macOS notification, email, or Slack DM à la job-sniper).
14. Git strategy: main-only vs. branches; auto-push policy for background jobs; recovery drill for a bad background commit.
15. Contract governance: process for bumping `.compose-contract` version when a new skill needs a new shared surface.

## 13. Roadmap: From Today to Up-and-Running

**Phase 0 — Prerequisites (one sitting).** Create the private GitHub repo. Install Claude Code + Git on the primary machine. Confirm Claude Code reads the local OneDrive Applications path. *Done when: repo clones and Claude Code opens it.*

**Phase 1 — Specification sprint (concurrent with Phase 2).** Hand this PRD to one session per workstream (A–D); each commits a spec to `/specs/`. Workstream A is the critical path. *Done when: four spec files exist and Charlie has ratified A.*

**Phase 2 — Scaffold + contract (sequential after 0; concurrent with 1).** Build the §5.1 skeleton: folders, `.compose-contract`, `AGENTS.md`, `CLAUDE.md`, command adapters, and stub SKILL.md files that execute end-to-end with placeholder output. *Done when: `/setup` runs and seeds `context/` + `memory/` stubs.*

**Phase 3 — Onboard + bootstrap the store (requires A-spec + Phase 2).** Run `/setup` for the interview-driven seeding of `context/` and `memory/`. Then the big value step: ingest the three source files, mine the OneDrive archive in place, ingest the LinkedIn CSV, and construct the `store/` CSVs (+ generated workbook). Charlie does one structured review pass — review, not data entry. *Done when: Charlie signs off on the store and it's committed.*

**Phase 4 — Light skills (concurrent with Phase 3).** Build *capture*, *writer-voice*, and *transcription-intake* — none depend on the career store. Seed `context/voice.md` with real samples. These deliver daily value immediately and start feeding `people/` before the engine exists. *Done when: a real transcript files correctly and a `/draft` passes the "sounds like me" test.*

**Phase 5 — Research skill (after Phase 2; before Phase 3 completes is fine).** Build the tiered *research* skill; run Brief tier against 2–3 known companies and tune the template; verify network overlay once `people/` has content. *Done when: a brief on a known company passes Charlie's quality bar.*

**Phase 6 — Career application engine (requires Phases 3 + 5).** Wire the full §7 workflow including write-back. Test the flywheel carefully — it is the product. *Done when: a dry run on an old, already-submitted posting reproduces or beats the manually produced quality.*

**Phase 7 — Background automation (after Phases 4–6 as each job's skill lands).** Install wrappers + scheduler definitions for the four §8 jobs, starting with *store-hygiene* and *transcript-sweep*. *Done when: a week of scheduled runs completes with clean logs and commits.*

**Phase 8 — Multi-endpoint + multi-runtime hardening (concurrent with 7).** Clone to machine 2; verify pull-edit-commit round trips on the CSVs; test phone kick-off of `/research`; run one skill end-to-end from a non-Claude agent via `AGENTS.md` (portability proof). *Done when: a run started on machine 2, phone, or a second runtime lands cleanly in the repo.*

**Phase 9 — Pilot + steady state.** Run 2–3 live applications end-to-end; measure attention-minutes, insights captured, and manual corrections (each correction is a template or store fix, not a one-off edit). Then: use for every application; read the weekly digest instead of maintaining the store; refresh the LinkedIn export quarterly.

**Critical path:** 0 → A-spec → 2 → 3 → 6 → 9. Phases 1B/1C/1D, 4, 5, 7, and 8 offer concurrency around it.
