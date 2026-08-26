# Workstream B — Research Spec
**Status:** Draft for ratification
**Governs:** the `research` skill (`/research`), both tiers, and the meeting-prep variant.

## 1. Tiers

| Tier | Invocation | Time/model | Output |
|---|---|---|---|
| **Quick** | `/research <question or name>` | Minutes; mid-tier model | Tight sourced answer, ≤400 words, in chat + optional file |
| **Brief** | `/research <company> --brief` | Deep pass; mid-tier model, top-tier permitted for priority targets | Full fixed-template company sheet at `research/<company>/brief-YYYY-MM-DD.md` |

Quick answers ground in `people/`, `memory/`, and `store/` first, then the live web, and label every claim's origin: **[memory]** vs **[web, date]**. If web access is unavailable, the skill says so and answers from memory only (degradation rule, PRD §10).

## 2. Brief template (fixed section set — comparability is the point)

1. **Snapshot** — one paragraph: what the company is, size, ownership, why it matters now.
2. **Business model & revenue** — how money is made; segments; rough scale.
3. **Ownership & financial condition** — public/PE/VC/family; recent raises, debt, distress signals.
4. **Leadership & board** — CEO and relevant CxOs; recent arrivals/departures; backgrounds.
5. **Strategy & recent moves** — 12–24 months of acquisitions, pivots, layoffs, launches.
6. **Technology / AI / transformation posture** — stack signals, AI stance, transformation maturity; job-posting language as evidence.
7. **Culture signals** — Glassdoor patterns, leadership language, turnover signals; clearly labeled as signals, not facts.
8. **Competitive landscape** — 3–5 named competitors and how the company differentiates.
9. **Risks** — the three things most likely to hurt them in 18 months.
10. **Network overlay** — every `people/` file whose frontmatter or notes connect to this company: primary (direct contact there) and secondary (person who can introduce). Names and file links only; note contents never quoted into external queries.
11. **Angles** — hooks connecting company needs to Charlie's proof points, each citing store entities by ID (e.g., "post-acquisition integration need ← acc-041, ins-012"). This section is what `/apply` consumes.

Every section carries a confidence marker (High/Medium/Low) and inline sources.

## 3. Source standards

- **Recency:** financial and leadership facts ≤12 months old or dated explicitly; anything older marked stale.
- **Multiplicity:** material claims (ownership, distress, leadership change) need two independent sources or a Low-confidence marker.
- **Conflicts:** presented side by side with dates — "Source A (2026-03) says X; Source B (2026-06) says Y" — never silently resolved.
- **Gemini Deep Research amplifier:** if `inbox/research-drops/` has a matching file, ingest it as *one source among many*: cross-examine against agent research, note agreements and contradictions in a short "Source review" appendix. Recommend a Gemini pass (don't require it) when the target is private with thin public data, or when the brief feeds a Deep-priority application.
- **People sensitivity:** searches may include public names and companies; never note contents.

## 4. Meeting-prep variant

`/research prep <person> [meeting context]` produces a two-minute pre-call brief:

1. Who they are (from `people/` frontmatter + web fill-in)
2. History with Charlie (from `## Notes`, most recent first)
3. What's open (action items from past transcripts involving them)
4. Company context (Snapshot-level, reusing an existing brief if ≤30 days old)
5. Three questions worth asking

Filed to `research/prep/<person>-YYYY-MM-DD.md`; a one-line dated note ("prep generated") appends to the person's file.

## 5. Write-backs (contract surfaces)

- Briefs and preps → `research/` (skill-owned).
- New people discovered (e.g., named CxOs relevant to an active thread) → new `people/` files with `source: research`, frontmatter only unless notes exist.
- Brief reuse: `/apply` and `/prep` reuse a brief ≤30 days old unless `--fresh` is passed; the brief file records generation date and model used.
