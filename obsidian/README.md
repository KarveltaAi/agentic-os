# Obsidian Vault Structure (agentic-os-vault)

The vault is a SEPARATE git repo so knowledge syncs independently of code.
Create these folders:

```
agentic-os-vault/
  00-Inbox/                  quick captures, unsorted
  05-Ideas/                  one file per idea (templates/idea.md) - Ben's /ideas intake
  10-Projects/               one note per project (index + links)
  20-Product/                PRDs, specs, research
  40-Delivery/
    Plans/                   /plan outputs
    Completion-Notes/        one note per finished story
    Handovers/               /handover outputs
    Backlog-Candidates.md    running list mirrored to ClickUp Backlog
  45-Development/            design docs, reviews, releases
  50-Security/               threat notes, review findings
  60-Legal/                  policies, licence reviews
  70-Marketing/              brand, GTM, SEO, email
  75-Media/                  social + print: strategy, copy, design specs, analytics
  90-Decisions/              ADRs + Board/ (boardroom transcripts)
```

Rules:
- Wikilinks between notes; every note that maps to ClickUp includes the ID.
- Sync = git. Install the community plugin "Obsidian Git" and set
  auto-commit/push (e.g. every 10 min) OR let /handover push at session end.
- Agents write to the vault through normal file tools; no plugin needed for
  Claude because the vault is just markdown on disk.
