# PROJECT.md template

> Copy into `projects/<slug>/PROJECT.md` and fill in every section. This file
> outranks the general agent library for project-specific work — see
> CLAUDE.md "Project-specific skills and agents".

## Client

- **Name:**
- **Type:** External client engagement / Self-owned product
- **Primary contact:** (name, role, email/Slack — "N/A, self-owned" if none)
- **Relationship owner (this side):**

## Scope

One paragraph: what the product/engagement is, who it's for, what it does.

## Deadlines

| Milestone | Date | Notes |
|---|---|---|
| | | |

## Stack

| Layer | Choice |
|---|---|
| | |

## IP / handover terms

- Who owns the code/IP at delivery?
- What does "handover" include (repo access, hosting transfer, docs, support window)?
- N/A if self-owned with no handover event planned.

## Confidentiality rule

Agents working this project must not reference other clients' code, data,
pricing, or names in any output produced for this project. Prefer one
client per session where possible.

## Project-specific agents/skills

List any agents in this repo's own `.claude/agents/` that outrank the
general library for this project, and any skills specific to it. "None yet"
is fine — propose new ones via `/new-agent` when a gap appears.

## Definition of Done (project-level, not story-level)

- [ ] Deployed
- [ ] Handover pack delivered (`templates/client-handover.md`) — skip if self-owned with no handover event
- [ ] `/retro <project>` run
