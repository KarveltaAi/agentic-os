# skills/ — Reusable How-To Library

A skill = one folder with a SKILL.md: a proven, repeatable procedure an
agent follows (e.g. "deploy a static site to Cloudflare Pages",
"client discovery call checklist", "Next.js project bootstrap").

```
skills/
  <skill-name>/
    SKILL.md        ← the procedure (required)
    assets/         ← templates, snippets (optional)
```

SKILL.md format:
---
name: <skill-name>
description: When to use this skill. Written so Ben/agents match on it.
---
Numbered steps, exact commands, gotchas, done-criteria.

Rules:
- Skills are born in retros: a thing that worked twice becomes a skill.
- Agents check skills/ before doing a task from scratch (rule in CLAUDE.md).
- Client-specific skills live in that client's repo, not here.
- Plain markdown = portable to any future agent runtime.
