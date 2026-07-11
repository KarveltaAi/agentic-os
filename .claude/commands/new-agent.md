---
description: Create a new agent in the library (general or project-specific)
argument-hint: <dept or project> <role name> <one-line scope>
---

Create a new agent: $ARGUMENTS

1. Copy templates/agent-template.md to the right home:
   - general: .claude/agents/<dept>/<role>.md
   - project-specific: <project>/.claude/agents/<role>.md (and list it in PROJECT.md)
2. Fill it in: description Ben can match on ("Use for X. Reports to Y."),
   minimal tools, concrete responsibilities, vault output path, and the
   mandatory completion-note clause.
3. Register it in library/registry.md (or the project's PROJECT.md).
4. Show the CEO the file for review before committing. No stealth hires.
