# Agentic OS Runbook v4.2 — Zero-to-Running in ~60 Minutes

Owner: Niyi Maku (CEO) · Target: a BRAND-NEW Windows 11 machine · Date: 2026-07-11 (v4.2 — 8-seat board incl. CTO/CMO/CAIO/DPO, shadow-board gate, 0.001% excellence standard)
Stack: Claude Code · ClickUp · Obsidian · Hermes 3 (Ollama) · GitHub
Cockpits: PowerShell · VS Code · Antigravity · Kiro (see docs/RUNTIMES.md)
Assumes you know NOTHING about the tools. Every command is copy-paste.

**Before you start, have these to hand:** your Claude account login, a GitHub
account (github.com/signup if none), a ClickUp account (clickup.com), and the
`agentic-os-scaffold.zip` file copied onto the new machine (USB stick or
download it from wherever you saved it).

---

## 0. What you are building (2 min read)

```
CEO (YOU — your brain, your voice)
 ├── ADVISORY BOARD (/boardroom): customer · investor · futurist · contrarian
 │      brainstorms, validates, stress-tests your ideas — visibly, turn by turn
 ├── BEN — Delivery Agent (main session, reports to you, mildly cheeky)
 │      plans → ClickUp stories → allocates → collects → reports
 │      ├── TASK-VALIDATOR: independent QA; FAIL loops work back (max 3, then escalates to you)
 │      ├── Product Dept:      product-manager + 9 roles
 │      ├── Development Dept:  dev-manager + 6 roles (fullstack-dev can run x2)
 │      ├── Security Dept:     security-manager + 4 roles
 │      ├── Legal & Compliance: legal-manager + 7 roles
 │      ├── Marketing Dept:    marketing-manager + 4 roles
 │      └── Media Dept:        media-manager + 10 roles (digital + print)
 └── PROJECT-SPECIFIC agents: live inside each project repo; Ben must use them
```

63 agents total, every one with a persona name (Petra runs Product, Deji
runs Development, Ada is your architect, Vera validates - full roster with
names: `library/registry.md`). The model pool works off-subscription: the Hermes crew (Hugo, Harriet,
Hector, Helga) runs on the LOCAL Hermes 3 model (free, private - Helga
redacts client PII on-machine), and Otto the model-router can escalate
offloads to budget or frontier models (Fable/GPT/Opus class) through
OpenRouter per ops/model-routing.json (Phase 4B).
Managers review, Ben dispatches, Vera audits, YOU decide. You can address
any agent by name by voice: "ask Ada to design the API".

How you SEE it working:
- Terminal: Ben prints `[HANDOVER]` / `[RETURN]` lines as agents exchange work,
  and Claude Code itself shows each subagent running.
- Dashboard: `python ops/dashboard.py` → http://localhost:8787 — active agents,
  sleeping agents, recent handovers, infra health. Auto-refreshes every 3s.

Why Ben is the main session and managers don't dispatch: Claude Code subagents
cannot spawn subagents. One orchestrator (Ben), everyone else is a specialist.

---

## Phase 1 — Install everything (minutes 0–12)

Click Start, type **PowerShell**, right-click → **Run as administrator**.
Paste this whole block, press Enter, and let it run:

```powershell
winget install --accept-package-agreements --accept-source-agreements Git.Git
winget install GitHub.cli
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install Ollama.Ollama
winget install Obsidian.Obsidian
winget install Microsoft.VisualStudioCode
```

Two more cockpits are downloads rather than winget (grab installers while
Hermes pulls, later in this phase): **Antigravity** from antigravity.google
and **Kiro** from kiro.dev/downloads. Both are optional for the first hour;
PowerShell alone runs everything.

(If winget itself is missing, install "App Installer" from the Microsoft
Store first, then rerun the block.)

**Close PowerShell and open a NEW one** (normal, not admin) so the installs
are picked up. Then install Claude Code:

```powershell
npm install -g @anthropic-ai/claude-code
```

Verify everything (each line should print a version, not an error):

```powershell
git --version; gh --version; node --version; python --version; ollama --version; claude --version
```

**Start Hermes downloading NOW in a second PowerShell window** (it is ~5 GB,
let it run in the background while you continue):

```powershell
ollama pull hermes3:8b
```

(Machine with under 16 GB RAM? Use `ollama pull hermes3:3b` instead.)

---

## Phase 2 — Sign in to Claude, GitHub, and set your identity (minutes 12–18)

```powershell
# GitHub — choose: GitHub.com → HTTPS → Login with a web browser
gh auth login

# Tell git who you are (used on every commit)
git config --global user.name  "Niyi Maku"
git config --global user.email "makniyi@gmail.com"

# Claude Code — first run opens a browser to sign in to YOUR Claude account
claude
```

When Claude Code opens and asks about theme/settings, accept defaults. Type
`exit` to leave it for now.

---

## Phase 3 — Create the OS from the scaffold (minutes 18–28)

```powershell
mkdir C:\AgenticOS
cd C:\AgenticOS
mkdir projects
```

Create the OS folder and unzip the scaffold into it (adjust the zip
filename/path to wherever you saved it, e.g. Downloads):

```powershell
mkdir C:\AgenticOS\agentic-os
Expand-Archive -Path "$env:USERPROFILE\Downloads\agentic-os-scaffold-v4.2.zip" -DestinationPath "C:\AgenticOS\agentic-os"
dir C:\AgenticOS\agentic-os\CLAUDE.md   # must exist before continuing
```

(If CLAUDE.md is missing but there is a single subfolder inside, the zip
was double-nested - move that subfolder's contents up one level.)

Then make it a GitHub repo:

```powershell
cd C:\AgenticOS\agentic-os
git init -b main
git add .
git commit -m "Agentic OS v2: Ben, board, validator, 6 departments, 52 agents"
gh repo create agentic-os --private --source . --push
```

Create the Obsidian vault (knowledge base) as its own repo:

```powershell
cd C:\AgenticOS
mkdir agentic-os-vault
cd agentic-os-vault
mkdir 00-Inbox, 10-Projects, 20-Product, 45-Development, 50-Security, 60-Legal, 70-Marketing, 75-Media, 90-Decisions
mkdir 40-Delivery\Plans, 40-Delivery\Completion-Notes, 40-Delivery\Handovers, 90-Decisions\Board
"# Backlog candidates" | Out-File 40-Delivery\Backlog-Candidates.md -Encoding utf8
git init -b main
git add .
git commit -m "Vault v1"
gh repo create agentic-os-vault --private --source . --push
```

Open **Obsidian** → "Open folder as vault" → `C:\AgenticOS\agentic-os-vault`.
Settings → Community plugins → turn on → Browse → install **"Git"**
(Obsidian Git) → enable it → in its options set "Auto commit-and-sync
interval" to 10 minutes. That is your vault sync.

---

## Phase 4 — Connect ClickUp (minutes 28–34)

In ClickUp (browser, app.clickup.com), create once:

```
Space: Agentic OS
  List: Backlog
  (a Folder per project later, each with a "Stories" list)
  Statuses on lists: todo / in progress / review / done / blocked
```

The scaffold already ships `.mcp.json` pointing at ClickUp's official MCP
server (`https://mcp.clickup.com/mcp`). Connect your account:

```powershell
cd C:\AgenticOS\agentic-os
claude
```

Inside Claude Code type:

```
/mcp
```

Select **clickup** → your browser opens → log in and authorise. Done. Test it:

```
Ben, show me the ClickUp workspace hierarchy
```

---

## Phase 4B — OpenRouter model tiers (optional, ~8 min, pay-as-you-go)

This gives Otto (the model-router agent) access to non-Claude models: cheap
ones for minimal tasks, frontier ones (Fable 5 / GPT 5.6 / Opus 4.8 class)
for heavy or strategic offloads and second opinions.

1. Create an account at openrouter.ai -> Keys -> create an API key.
   IMPORTANT: also set a monthly spend limit in the account settings.
2. In the repo: copy `.env.example` to `.env` and paste the key in.
   (.env is gitignored and read-denied to agents; keep it that way.)
3. Pick real model IDs at openrouter.ai/models and replace the placeholders
   in `ops/model-routing.json` (one budget model, one frontier model).
4. Test both tiers:

```powershell
python scripts\llm.py --tier local "say ready"
python scripts\llm.py --tier budget "say ready"
```

5. Inside Claude Code: `ask Otto for a frontier second opinion on <topic>`
   - Otto routes it, quality-checks it, and logs which tier and why.

Skip this phase entirely and everything still works - Otto simply reports
that only the local tier is configured.

---

## Phase 5 — Smoke test the whole organisation (minutes 34–50)

Stay inside Claude Code (`claude` from `C:\AgenticOS\agentic-os`).

**5.1 The roster is alive:**

```
/agents
```

You should see the departments' agents (task-validator, board seats,
managers, roles). If not: you launched claude outside the repo folder.

**5.2 Board meeting (watch them argue):**

```
/boardroom A subscription box for left-handed guitarists in the UK
```

Expected: each seat speaks in turn under its own header, a rebuttal round,
a PURSUE/PIVOT/PARK verdict table, Ben's synthesis, transcript saved to the
vault, and "Your call, chief."

**5.3 The full pipeline (idea -> release plan):**

```
/ideas
```

(Empty first time - create an idea note in the vault 05-Ideas/ from
templates/idea.md, or just say: "Ben, add an idea: waitlist site for
product X", then rerun /ideas.) Then follow the pipeline: /boardroom
(8 seats speak in turn, contrarian closes) -> /discover DemoProject <idea>
-> CEO approval -> /shadow-review DemoProject (Hera's local bench critiques
the decision; any CHALLENGE goes back to you) -> /plan DemoProject.
The shadow-board roster is placeholder seats until you provide your own:
edit ops/shadow-board.json.
Expected in ClickUp: epics as parent tasks, stories as subtasks, every
title starting DEM-001, DEM-002..., dependencies linked, and
planning/release-plan.md in the project folder.

Shortcut for tiny work (CEO explicit): skip discovery -

```
/plan DemoProject Build a one-page waitlist site for product X
```

Approve the stories when shown. Then take one ClickUp ID from the plan:

```
/build <that-ID>
```

Watch for: `[HANDOVER]` line → role agent works → manager review →
task-validator verdict. If FAIL, you will see the defect list and the loop
counter (n/3) as it goes back.

**5.4 The dashboard (second PowerShell window):**

```powershell
cd C:\AgenticOS\agentic-os
python ops\dashboard.py --share
```

(`--share` publishes this machine's events through GitHub every 60s so the
other operator's dashboard can see them. Without it the dashboard is
read-only: your live events + whatever the other machine last pushed.)

Open http://localhost:8787 in a browser. You should see the active agent(s)
from your /build, the handover feed, sleeping agents, and infra checks
(Ollama, disk, git, ClickUp).

**5.5 Hermes sidecar (once the pull from Phase 1 finished):**

```powershell
.\scripts\hermes.ps1 "Say ready if you can hear me"
```

Then test the crew end-to-end inside Claude Code:

```
have Hugo summarise the RUNBOOK.md in five bullets
```

**5.6 Ops in the terminal:**

```
/ops
```

---

## Phase 6 — Voice commands (minutes 50–55)

Voice = dictation into the Claude Code terminal. CLAUDE.md maps natural
speech to workflows, so you can literally say "Ben, board meeting about the
guitar box idea".

- **Free, built in:** click into the terminal, press `Win+H`, speak.
- **Better:** Wispr Flow for Windows (wisprflow.ai) — hotkey
  `Ctrl+Shift+Space`, removes filler words, free tier 2,000 words/week,
  Pro ~$15/month. Known issue: one Claude Code release (v2.1.83) broke its
  text injection on Windows (github.com/anthropics/claude-code/issues/38620);
  if that hits you, update Claude Code or fall back to Win+H.

Speaking style: end commands with a verb. "Ben, status." "Ben, build story
86-x-y." Ben confirms his interpretation in one line before acting.

---

## Phase 6A — The four cockpits (optional in the hour, ~10 min each)

The OS runs from any of four front-ends. Full capability matrix and rules:
`docs/RUNTIMES.md`. Short version: Claude Code (terminal or VS Code) runs
the FULL machinery (Ben, subagents, /commands, validation loops, dashboard
events). Antigravity and Kiro are coding cockpits: they read the generated
AGENTS.md automatically and talk to ClickUp over MCP, but Ben's
orchestration and the dashboard hooks do not run there.

**VS Code (full OS in an IDE):**
1. Open VS Code → Extensions → install "Claude Code" (it is also in this
   repo's .vscode/extensions.json recommendations).
2. File → Open Folder → `C:\AgenticOS\agentic-os` (or a project repo).
3. Open the Claude Code panel and use it exactly like the terminal:
   /plan, /build, /boardroom, voice via Win+H into the panel.

**Antigravity (Google, Gemini agents):**
1. Install from antigravity.google, sign in with a Google account.
2. Open `C:\AgenticOS\agentic-os` (or a project repo) as a workspace —
   it reads AGENTS.md automatically (v1.20.3+).
3. One-time per machine: Settings → Customizations → MCP → add ClickUp
   (`https://mcp.clickup.com/mcp`); stored in ~/.gemini/config/mcp_config.json.

**Kiro (AWS, spec-driven agents):**
1. Install from kiro.dev/downloads, sign in.
2. Open the repo — AGENTS.md is picked up automatically and
   `.kiro/settings/mcp.json` (ClickUp) ships in the repo.

**Cross-cockpit rules (memorise these two):**
- CLAUDE.md is the master; after editing it run
  `python scripts/sync-runtimes.py` and commit (retros do this for you).
- Work done in Antigravity/Kiro is invisible to the dashboard, so update
  the ClickUp task and write the completion note yourself, or tell Ben
  afterwards and he backfills. ClickUp is the cross-runtime truth.

---

## Phase 7 — Colleague onboarding (later, ~15 min, not in the hour)

1. You: `gh repo edit agentic-os --add-collaborator <their-github-username>`
   and the same for `agentic-os-vault`. Invite their email to the ClickUp
   workspace as a member.
2. They: run Phases 1–2 on their machine (their OWN Claude account —
   Claude logins cannot be shared), then:

```powershell
mkdir C:\AgenticOS; cd C:\AgenticOS; mkdir projects
gh repo clone <your-username>/agentic-os
gh repo clone <your-username>/agentic-os-vault
cd agentic-os
claude
/mcp     (authorise ClickUp with THEIR ClickUp login)
```

3. They open the vault in Obsidian + install Obsidian Git, same settings.
4. Cockpits are per-person taste: they can use any of the four (Phase 6A);
   Antigravity/Kiro MCP sign-ins are per machine.

The agents respond to you both identically because they are repo files.
Collision rules: `git pull` at session start, `/handover` at session end,
different stories per operator, ClickUp assignment shows ownership.

**Shared dashboard:** both of you run `python ops\dashboard.py --share`.
Each machine logs to its own `ops/events-<machine>.jsonl` (no merge
conflicts) and pushes every 60s; each dashboard merges both files, with a
"machine" column showing who is doing what. Remote view lags by up to a
minute - that is the price of zero infrastructure. If you ever want the
other person's dashboard truly live, a free private-network tool like
Tailscale lets you open their localhost:8787 directly (check current plan
terms).

---

## Phase 8 — Project-specific agents and skills

Each project repo can carry its own specialists:

```
projects/<name>/
  PROJECT.md            ← lists the project's agents, skills, context
  .claude/agents/       ← project-specific agents (e.g. stripe-integrator.md)
```

Create one: `/new-agent <project> <role> <scope>`. Ben's rules (in CLAUDE.md
and /plan//build) force him to read PROJECT.md first and allocate to project
agents where they fit — he acknowledges them by name in the allocation table.

Note: when Ben works INSIDE a project folder, that project's agents load
automatically; from the OS repo he reads their definitions from PROJECT.md.

---

## Phase 9 — Daily rhythm

```
Morning   git pull (OS + vault) → claude → /status → /ops
Ideate    /boardroom <idea>                 (board argues, you decide)
Plan      /plan <project> <goal>            (approve before ClickUp writes)
Deliver   /build <ID>, <ID>                 (watch handovers; validator loops)
Review    read completion notes; accept or bounce
Weekly    /groom
End       /handover                          (writes notes, pushes everything)
```

Definition of done (validator-enforced): criteria met, work verified to
exist and be right, completion note in vault, ClickUp updated, new backlog
items logged.

## Guardrails

- Secrets only in `.env`/`secrets/` (gitignored + read-denied to Claude).
- Ben shows plans/grooming BEFORE writing to ClickUp. Board advises, CEO decides.
- security-manager veto on Critical findings; legal RED = human solicitor.
- Validator escalates to CEO after 3 failed loops — no infinite hamster wheels.
- External sends (posts, emails, ads, money) are CEO-only actions.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `winget not recognised` | Install "App Installer" from Microsoft Store, reopen PowerShell |
| `claude not recognised` | Reopen PowerShell after npm install; check `npm bin -g` is on PATH |
| /agents shows nothing | You are not in `C:\AgenticOS\agentic-os`; `cd` there and rerun `claude` |
| /mcp clickup fails | Re-run /mcp and re-authorise; corporate firewalls can block OAuth |
| Dashboard empty | It fills as hooks log events; run a /build first. Check `ops/events.jsonl` exists |
| Hooks not logging | `python --version` works? Reopen terminal; hooks call `python ops/log_event.py` |
| Hermes hangs | Ollama not running: start the Ollama app or `ollama serve` |
| Voice text not appearing | Focus the terminal before Win+H; Wispr issue → see Phase 6 |
| Vault merge conflicts | Pull before session; resolve in Obsidian Git or plain git |

## Sources

- Claude Code docs (install, subagents, hooks, MCP): https://docs.claude.com/en/docs/claude-code
- ClickUp official MCP: https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server
- Hermes 3 on Ollama: https://ollama.com/library/hermes3
- Wispr Flow: https://wisprflow.ai/use-cases/claude

---

## Phase 10 — Agency mode, cost, portability, self-improvement (added v2.1)

**Client work:** every client engagement starts with
`/client-project <client> <project> <brief>` — it creates an isolated repo,
ClickUp folder, vault folder and PROJECT.md with confidentiality rules.
Project done = deployed + handover pack (templates/client-handover.md) +
`/retro <project>`. Zero-cost client hosting: see skills/ship-static-site.

**Where the OS lives:** on your machine (local-first), synced through GitHub.
Nothing runs in a cloud you pay for. If you later need always-on scheduled
runs (nightly /backup, weekly /status), a small VPS (e.g. Hetzner/Contabo,
a few pounds/month — check current pricing) can clone the same repos and run
the same commands; the OS is just git repos, so it moves anywhere.

**Costs:** ClickUp Free tier, GitHub free private repos, Obsidian free +
Obsidian Git, Ollama/Hermes free, Win+H free, dashboard free. Standing cost
= your Claude subscription. Protect usage: Hermes for bulk text,
`model: haiku` frontmatter for mechanical agents, short focused sessions.

**No lock-in:** agents/skills/knowledge are plain markdown in git (portable
by design). Run `/backup` weekly so ClickUp state also lives in the vault.
Client repos must deploy without this OS.

**Self-improvement:** `/retro` (weekly + per project) turns evidence from
ops/events.jsonl and completion notes into approved edits to agents, skills
and templates, logged in library/improvement-log.md. The OS you have in
December should embarrass the one you built today.
