---
name: research
description: Tiered research - quick sourced answers, full company briefs, and meeting prep.
commands: ["/research"]
writes: ["research/", "people/ (new files + #Notes)"]
model: mid
interactive: false
---

# Research — quick answers, deep briefs, meeting prep

Governed by `specs/research-spec.md` — read it before a Brief-tier run; the template and source standards there are the contract.

## Purpose
One skill, three modes:
- **Quick** (default): `/research <question or name>` — a tight, sourced answer, ≤400 words.
- **Brief:** `/research <company> --brief` — the full fixed-template company research sheet.
- **Prep:** `/research prep <person> [context]` — a two-minute pre-call brief.

## Inputs
- The query. Memory first: `people/`, `memory/`, `store/`, existing `research/` output. Then the live web.
- Optional amplifier: a matching file in `inbox/research-drops/` (e.g., Gemini Deep Research output) — treated as one source among many and cross-examined.

## Steps
**Quick:** ground in memory, fill from web, answer with every claim labeled **[memory]** or **[web, date]**. Save to `research/notes/<slug>-YYYY-MM-DD.md` only if asked or the answer is clearly reusable.

**Brief:** follow the 11-section template in `specs/research-spec.md` §2 exactly (comparability across companies and time is the point). Confidence marker per section; two independent sources for material claims; conflicts shown side by side, dated. The **Network overlay** section scans `people/` frontmatter and notes for connections — names and file links in the output, note contents never quoted into any external query. The **Angles** section cites store entities by ID. File to `research/<company-slug>/brief-YYYY-MM-DD.md`. Reuse a brief ≤30 days old instead of regenerating, unless `--fresh`.

**Prep:** the five-part brief in `specs/research-spec.md` §4, built from the person's file first, web second. File to `research/prep/<person>-YYYY-MM-DD.md`; append a one-line dated "prep generated" note to their `people/` file.

## Write-backs
Only surfaces in `writes:`. Newly relevant people discovered (e.g., a CxO at a target company) get frontmatter-only `people/` files, `source: research`. Commit: `research(<subject>): <tier>`.

## Self-seed behavior
Missing folders → create. Empty `people/` → briefs simply have an empty network overlay, stated as such.

## Failure behavior
No web access → answer from memory only and say so explicitly, per claim. Thin public data on a private company → say what couldn't be established rather than padding; recommend a Gemini Deep Research pass when the spec's criteria (§3) are met.
