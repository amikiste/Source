# People

One file per person: `<kebab-full-name>.md`. Schema and matching rules: `specs/store-conventions.md` §6. Skills append dated notes under `## Notes` and keep frontmatter current; they never rewrite history. This folder is the most sensitive data in the repo — its contents are never quoted into web searches or external services.

Template for new files:

```markdown
---
name: {Full Name}
aliases: []
company: {unknown}
role: {unknown}
relationship: {unknown}
context_met: {unknown}
last_touched: {YYYY-MM-DD}
source: {linkedin-export | transcript | application | research | capture | manual}
---

# {Full Name}

## Notes
```
