# Agent Library Registry (v4.2)

v5 — Gitflow, Vera's rework loop in ClickUp, completion notes as gates. Single source of truth for every agent. /new-agent appends here (and must
assign a persona name). Every agent operates to the top-0.001% excellence
standard (see CLAUDE.md). Address agents by name in voice commands.
Project agents live in each PROJECT.md. Runtimes: docs/RUNTIMES.md.
Model pool + Shadow Board run on the LOCAL model; Otto can escalate
offloads via OpenRouter per ops/model-routing.json.

| Name | Agent (file) | Department | Scope | Status |
|---|---|---|---|---|
| Ben | ben | Delivery (main session) | Orchestration, pipeline, ClickUp, reporting | Active |
| Paige | planner | Delivery (planning) | Feature>Epic>Story>Task decomposition, IDs, dependencies, release plan | Active |
| Vera | task-validator | Delivery (independent QA) | Verifies work exists, is done, is right; PASS/FAIL loop | Active |
| Dupe | board-dpo | Advisory Board | Advisory Board seat | Active |
| Kai | caio | Advisory Board | Advisory Board seat | Active |
| Mona | cmo | Advisory Board | Advisory Board seat | Active |
| Cassandra | contrarian | Advisory Board | Advisory Board seat | Active |
| Tayo | cto | Advisory Board | Advisory Board seat | Active |
| Priya | customer | Advisory Board | Advisory Board seat | Active |
| Felix | futurist | Advisory Board | Advisory Board seat | Active |
| Victor | investor | Advisory Board | Advisory Board seat | Active |
| Hera | shadow-chair | Shadow Board (local model) | Shadow board chair | Active |
| Hector | hermes-classifier | Model pool (local + OpenRouter) | Hermes crew (local model) | Active |
| Harriet | hermes-drafter | Model pool (local + OpenRouter) | Hermes crew (local model) | Active |
| Helga | hermes-redactor | Model pool (local + OpenRouter) | Hermes crew (local model) | Active |
| Hugo | hermes-summariser | Model pool (local + OpenRouter) | Hermes crew (local model) | Active |
| Otto | model-router | Model pool (local + OpenRouter) | Model pool dispatcher | Active |
| Petra | product-manager | Product | Product department manager | Active |
| Abe | ab-tester | Product | Product department role | Active |
| Bisi | business-analyst | Product | Product department role | Active |
| Kofi | competitor-researcher | Product | Product department role | Active |
| Dana | data-analyst | Product | Product department role | Active |
| Ivy | investment-analyst | Product | Product department role | Active |
| Mara | market-researcher | Product | Product department role | Active |
| Pablo | pitch-developer | Product | Product department role | Active |
| Sophie | spec-writer | Product | Product department role | Active |
| Uche | ux-designer | Product | Product department role | Active |
| Deji | dev-manager | Development | Development department manager | Active |
| Ada | architect | Development | Development department role | Active |
| Bayo | backend-dev | Development | Development department role | Active |
| Ray | code-reviewer | Development | Development department role | Active |
| Dara | devops-release | Development | Development department role | Active |
| Femi | fullstack-dev | Development | Development department role | Active |
| Uma | uiux-dev | Development | Development department role | Active |
| Sade | security-manager | Security | Security department manager | Active |
| Aisha | appsec-reviewer | Security | Security department role | Active |
| Hana | compliance-hardener | Security | Security department role | Active |
| Didi | dependency-auditor | Security | Security department role | Active |
| Tunde | threat-modeller | Security | Security department role | Active |
| Lola | legal-manager | Legal & Compliance | Legal & Compliance department manager | Active |
| Bode | bid-specialist | Legal & Compliance | Legal & Compliance department role | Active |
| Carla | contracts-reviewer | Legal & Compliance | Legal & Compliance department role | Active |
| Dami | dpo | Legal & Compliance | Legal & Compliance department role | Active |
| Halima | health-compliance-officer | Legal & Compliance | Legal & Compliance department role | Active |
| Ike | ip-licensing | Legal & Compliance | Legal & Compliance department role | Active |
| Remi | regulatory-scanner | Legal & Compliance | Legal & Compliance department role | Active |
| Rita | rfi-rfp-specialist | Legal & Compliance | Legal & Compliance department role | Active |
| Maya | marketing-manager | Marketing | Marketing department manager | Active |
| Bella | brand-positioning | Marketing | Marketing department role | Active |
| Emma | email-crm | Marketing | Marketing department role | Active |
| Greg | growth-gtm | Marketing | Marketing department role | Active |
| Seyi | seo-web | Marketing | Marketing department role | Active |
| Chidi | community-manager | Media | Media department role | Active |
| Mide | media-manager | Media | Media department manager | Active |
| Paddy | paid-ads-manager | Media | Media department role | Active |
| Amara | brand-ambassador | Media | Media department role | Active |
| Prosper | content-producer | Media | Media department role | Active |
| Cleo | content-strategist | Media | Media department role | Active |
| Wale | copywriter | Media | Media department role | Active |
| Pippa | print-graphic-designer | Media | Media department role | Active |
| Sana | social-analyst | Media | Media department role | Active |
| Coco | social-coordinator | Media | Media department role | Active |
| Gigi | social-graphic-designer | Media | Media department role | Active |

## Conventions

- One agent = one file under `.claude/agents/<dept>/`, lowercase-hyphenated.
- Every agent has a persona name and the top-0.001% excellence standard.
- Description = what Ben matches on. Minimum tools per agent. `model:`
  frontmatter sets Claude tier (haiku for mechanical roles).
- Managers review; Ben dispatches; Paige plans; Vera audits; Hera's shadow
  board (seats: ops/shadow-board.json, CEO-defined) gates decisions before build.
- ClickUp item titles: PREFIX-NNN (3 letters of project + 3 digits, 4 past 999).
- fullstack-dev runs as parallel twins Femi-1 and Femi-2.
- Retire agents to `library/retired/` and mark Status here.
