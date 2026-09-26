# Agentic OS Runbook v5.0 — Zero-to-Running in ~60 Minutes

Owner: Niyi Maku (CEO) · Target: a BRAND-NEW Windows 11 machine · Date: 2026-09-26 (v5.0: solo git flow with no PR approvals, 5 model tiers incl. free and media (image/voice/Veo/HeyGen), Hermes CPU-speed routing, Windows gotchas. v4.2: 8-seat board, shadow-board gate, 0.001% excellence standard)
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
 ├── ADVISORY BOARD (/boardroom): customer · investor · futurist · CTO · CMO · CAIO · DPO · contrarian
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
names: `library/registry.md`). The model pool works off-subscription, routed
by Otto per `ops/model-routing.json` (Phase 4B):

| Tier | What | Cost |
|---|---|---|
| local | Hermes 3 on your machine (Ollama). ALL private data. Helga redacts here only | Free |
| budget | 6 free OpenRouter models, tried in order. Never client data | Free |
| research | Hermes 4 405B, Sonar Deep Research (live web) | Mid |
| frontier | Opus, GPT, Kat-Coder, Fable | Premium |
| media | Images, voice, Veo video, HeyGen talking video (`scripts/media.py`) | Pennies per asset |

The Hermes crew (Hugo, Harriet, Hector) keeps private work local and sends
long non-private text to the free budget tier, because the local model is
slow on a laptop CPU (about 1 minute per page).
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
winget install Microsoft.PowerShell
```

From now on open **PowerShell 7** (Start → "PowerShell 7"), not the old
"Windows PowerShell". The old one rejects `&&` between commands.

**Stop the Python trap (one-time, 1 min):** Settings → Apps → Advanced app
settings → **App execution aliases** → turn OFF `python.exe` and
`python3.exe`. Otherwise `python3` opens the Microsoft Store instead of
running Python. Agents are told to use `python`, never `python3`.

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

**Speed expectation:** without a supported GPU (e.g. Intel laptop graphics),
Hermes runs on the CPU at roughly 7 tokens/s reading and 2 writing: fine
for short jobs, about 1 minute per page for long ones. That is why the crew
routes long non-private text to the free budget tier.

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
git commit -m "Agentic OS v5: Ben, 8-seat board, validator, 6 departments, 63 agents"
gh repo create agentic-os --private --source . --push
git checkout -b dev
git push -u origin dev
```

**Git flow (solo):** you work on `dev`; `/gitflow release` fast-forwards
`main` to `dev`. No pull requests, no approvals. **Do NOT add GitHub branch
rules that require a PR review:** GitHub will not let you approve your own
PR, so with one operator every release gets stuck. The only rule worth
adding on `main` is "block force pushes" + "restrict deletions"
(repo → Settings → Rules → Rulesets). If a second operator joins, bring
reviews back deliberately via /retro.

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

## Phase 4B — OpenRouter model tiers (optional, ~10 min, pay-as-you-go)

This gives Otto (the model-router agent) the budget, research, frontier and
media tiers from section 0. One OpenRouter key covers all of them,
including Veo and HeyGen talking video.

1. Create an account at openrouter.ai → Keys → create an API key. On that
   key, set a **credit limit** (e.g. $5/month).
2. **Add credits** (Credits page, ~$5). With zero credits only the free
   budget tier works; everything else returns `402 Insufficient credits`.
3. In the repo: copy `.env.example` to `.env` and paste the key after
   `OPENROUTER_API_KEY=` (edit with `code .env`, never Notepad).
   `.env` is gitignored and read-denied to agents; keep it that way.
4. `ops/model-routing.json` ships with model IDs verified on 2026-09-26.
   IDs change: if a tier errors with 400/404 "model", check
   openrouter.ai/models (text) or the Videos API models list (video) and
   update the `"model"` list. Each tier lists several models tried in order,
   so one bad or rate-limited model falls through to the next.
5. Test every tier (each should print "ready" and name the model used):

```powershell
python scripts\llm.py --tier local "say ready"
python scripts\llm.py --tier budget "say ready"
python scripts\llm.py --tier research "say ready"
python scripts\llm.py --tier frontier "say ready"
```

   Free models are often rate-limited (you will see "failed, trying next");
   that is normal. Rerun if all six are busy.

6. Inside Claude Code: `ask Otto for a frontier second opinion on <topic>`
   - Otto routes it, quality-checks it, and logs which tier and why.

**Optional HeyGen key:** talking-head video already works through
OpenRouter. Add `HEYGEN_API_KEY` to `.env` (app.heygen.com → Settings → API)
only for your own HeyGen avatars or a cloned voice.

Skip this phase entirely and everything still works - Otto simply reports
that only the local tier is configured.

---

## Phase 5 — Smoke test the whole organisation (minutes 34–50)

Stay inside Claude Code (`claude` from `C:\AgenticOS\agentic-os`).

**5.1 The roster is alive:** (the old `/agents` screen was removed from
Claude Code, so ask Ben instead)

```
Ben, list every subagent type you can dispatch, grouped by department
```

You should see the departments' agents (task-validator, board seats,
managers, roles, the Hermes crew, model-router). If not: you launched
claude outside the repo folder.

**Golden rule:** after anything edits files in `.claude/agents/` (a
`/retro`, `/new-agent`, or a manual edit), **exit and restart `claude`**.
A running session only partly reloads edited agents, and some go missing
with "Agent type not found".

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
python scripts\llm.py --tier local "Say ready if you can hear me"
```

(First run takes 20-40s while the model loads.) Then test the crew
end-to-end inside Claude Code:

```
have Hugo summarise the RUNBOOK.md in five bullets
```

Expected: under a minute, labelled "via budget". The runbook is long and
not private, so Hugo sends it to the free tier. A private document would
stay local and take minutes; Hugo warns you of the time first.

**5.6 Ops in the terminal:**

```
/ops
```

**5.7 Media tier (needs Phase 4B credits; ~$0.40 total):**

```powershell
python scripts\media.py image "flat minimalist orange fox logo on white"
python scripts\media.py voice "Karvelta. Shipping with ease."
python scripts\media.py video "slow pan over a Manchester canal at dusk"
python scripts\media.py talking "Hi, I'm your assistant." --photo media-out\<a-photo>.jpeg --aspect 9:16
```

Files land in `media-out\` (gitignored). Costs: image and voice under 1p,
an 8s Veo Lite clip ~$0.40, talking video $0.05/second. Use `--no-audio`
for cheaper silent clips. Only animate a real person's photo with their
written consent; nothing generated is published without CEO sign-off.

**5.8 Release (solo flow):**

```
/gitflow release
```

Ben asks "Ship N commits from dev to main?"; say yes. `/gitflow` on its own
shows what is waiting.

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
Release   /gitflow release                   (dev → main, no PR)
Weekly    /groom · /retro (then RESTART claude) · /backup
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
- Private or client data never goes to the free budget tier (providers may
  log prompts). When in doubt it stays local; Helga is local-only, always.
- Generated media (media-out/) needs CEO sign-off before publishing; no real
  person's face or voice without written consent.
- OpenRouter spend is capped by the credit limit on your key; Otto states
  the cost before any 1080p/4K or batch video run.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `winget not recognised` | Install "App Installer" from Microsoft Store, reopen PowerShell |
| `claude not recognised` | Reopen PowerShell after npm install; check `npm bin -g` is on PATH |
| No agents / "Agent type not found" | Not in `C:\AgenticOS\agentic-os` → `cd` there. Or agent files were edited mid-session (e.g. by /retro) → exit and restart `claude` |
| `/agents` says "wizard has been removed" | Expected: use the Phase 5.1 prompt to list agents |
| `'&&' is not a valid statement separator` | You are in old Windows PowerShell 5.1: open PowerShell 7, or run the commands one per line |
| `python3` opens the Store / "Python was not found" | Use `python`; turn off the App execution aliases (Phase 1) |
| Typing `/build` in PowerShell → "not recognized" | Slash commands only work inside Claude: run `claude` first |
| Hermes/Hugo very slow or "timed out" | CPU-only local model (~1 min/page). Non-private text → budget tier; private → chunk it, or add `--timeout 900` |
| `402 Insufficient credits` | Add OpenRouter credits (Phase 4B step 2) |
| `429` / "failed, trying next" on budget | Free models rate-limited; normal. The chain falls through; rerun if all fail |
| `400`/`404` mentioning the model | Model ID changed: update `ops/model-routing.json` (Phase 4B step 4) |
| PR stuck "Review required" | A branch rule demands approval; you cannot self-approve. Remove it (Phase 3 git flow note) and use `/gitflow release` |
| ClickUp updates stall for hours | ClickUp MCP daily call limit hit (observed ~100/day). Wait for the reset; /build already caps backlog-task creation. Sync statuses first, extras later |
| /mcp clickup fails | Re-run /mcp and re-authorise; corporate firewalls can block OAuth |
| Dashboard empty | It fills as hooks log events; run a /build first. Check `ops/events-<machine>.jsonl` exists |
| Hooks not logging | `python --version` works? Reopen terminal; hooks call `python ops/log_event.py` |
| Hermes hangs | Ollama not running: start the Ollama app or `ollama serve` |
| Voice text not appearing | Focus the terminal before Win+H; Wispr issue → see Phase 6 |
| Vault merge conflicts | Pull before session; resolve in Obsidian Git or plain git |

## Sources

- Claude Code docs (install, subagents, hooks, MCP): https://docs.claude.com/en/docs/claude-code
- ClickUp official MCP: https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server
- Hermes 3 on Ollama: https://ollama.com/library/hermes3
- Wispr Flow: https://wisprflow.ai/use-cases/claude
- OpenRouter docs (models, images, video generation): https://openrouter.ai/docs
- HeyGen API (optional direct route): https://developers.heygen.com

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
Obsidian Git, Ollama/Hermes free, Win+H free, dashboard free, 6 free
OpenRouter models. Standing cost = your Claude subscription, plus
pay-as-you-go OpenRouter credits for research/frontier/media (capped by
your key's credit limit). Protect usage: Hermes and the free tier for bulk
text, `model: haiku` frontmatter for mechanical agents, short focused
sessions.

**No lock-in:** agents/skills/knowledge are plain markdown in git (portable
by design). Run `/backup` weekly so ClickUp state also lives in the vault.
Client repos must deploy without this OS.

**Self-improvement:** `/retro` (weekly + per project) turns evidence from
ops/events-<machine>.jsonl and completion notes into approved edits to agents, skills
and templates, logged in library/improvement-log.md. The OS you have in
December should embarrass the one you built today.
