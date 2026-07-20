# Completion note template

> Copy to `<vault>/40-Delivery/Completion-Notes/<STORY-ID>.md` when closing
> a story (delivery loop step 6, CLAUDE.md). One file per story — do not
> fold this content into another artefact's own "completion note" section
> (e.g. a runbook or spec doc); the standalone file at this path is what
> gates forwarding to task-validator, not an embedded section elsewhere.
>
> **Before forwarding to the validator, re-read the frontmatter, the
> header block, and the Review loop section together and confirm they
> agree with each other and with what actually happened.** The most
> common validator FAIL on this OS so far has been the completion note
> contradicting itself (frontmatter `status` vs. header `Loop` line vs.
> the body's own account) — not the underlying deliverable. A 30-second
> self-check here is cheaper than a rework loop.

```markdown
---
project: <ProjectName>
story: <STORY-ID>
title: <story title, matches ClickUp task name>
status: in review   # to do | in progress | in review | done
date: YYYY-MM-DD
release: <R0 | R1 | ... — from the release plan>
tags: [feature:<slug>, department:<dept>, ...]
---

# <STORY-ID> — <story title>

*Karvelta — Shipping with ease*

**ClickUp:** [<task-id>](<task-url>) · <List name>
**Epic:** <parent epic ID + title>
**Allocation:** <named agent(s), per the release plan's allocation table>
**Loop:** <N>/3 (<one-line summary of rework/FAIL cycles so far, or "no
rework cycles yet">)

## What was delivered

<What the story actually shipped — files, decisions, artefacts. Reference
the acceptance criteria by number or by clear paraphrase; don't just
restate them.>

## Review loop

<Numbered, chronological account of every step: implement, each manager
review (verdict + what it found), each fix, each validator pass (verdict
+ defect list if FAIL). Update this section EVERY time the story goes
through another loop — do not let it go stale while other sections move
on. This is the section most likely to drift from the header/frontmatter;
re-read all three together before every resubmission.>

1. **Implement (loop 1):** ...
2. **Manager review — <name>:** APPROVE | REWORK (<N> fixes) ...
3. ...

## Assumptions made

<Judgment calls made without an explicit upstream instruction, and why.
Flag scope divergences here even if a reviewer later confirms they were
correct — the note should show the reasoning, not just the outcome.>

## Risks

<Residual risk, labelled H/M/L, with what would need to happen for it to
matter and who owns watching for it.>

## New backlog candidates

<Anything surfaced by this story that isn't in scope for it. Cross-check
against the release plan's own backlog list first — don't re-log an item
that was already flagged at planning time.>

## Files touched

<Every file created or edited by this story, with a one-clause note on
what changed if not obvious from the path.>

**Operator:** <CEO name or co-operator, per session>
```
