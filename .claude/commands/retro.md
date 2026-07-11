---
description: Retrospective that upgrades the OS - agents, skills and process improve from evidence
argument-hint: <project name, or "weekly">
---

Act as Ben. Run a retro for: $ARGUMENTS

1. EVIDENCE, not vibes. Pull:
   - ops/events.jsonl: dispatch counts, validation FAIL rate per agent,
     stories that hit loop 2+ or escalated
   - Completion notes: recurring assumptions and risks
   - ClickUp: cycle time per story where visible; blocked history
2. Diagnose: for each recurring failure, name the SYSTEM cause — unclear
   agent instructions? missing skill? bad story writing? wrong allocation?
3. Propose upgrades as a diff list, each one of:
   - EDIT an agent .md (tighten instructions, add a rule)
   - ADD a skill to skills/ (repeatable how-to the agent should follow)
   - EDIT a command or template
   - RETIRE something unused
4. Show the CEO the proposed diffs. On approval: apply; if CLAUDE.md changed,
   run `python scripts/sync-runtimes.py` so AGENTS.md follows; log each change in
   library/improvement-log.md (date, change, evidence, expected effect),
   commit as "retro: <summary>".
5. Close with one metric to watch before the next retro.
