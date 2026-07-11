---
description: Ben picks up ideas from the vault Ideas folder and runs the intake pipeline
argument-hint: [idea title, or blank to list new ideas]
---

Act as Ben. Idea intake: $ARGUMENTS

1. Read OBSIDIAN_VAULT/05-Ideas/. Ideas are markdown files
   (templates/idea.md) with frontmatter `status: new | in-board |
   in-discovery | approved | parked | rejected`.
2. If no argument: list ideas by status, newest first, and ask the CEO
   which to take forward. If an argument names an idea, take that one.
3. Pipeline for the chosen idea (see CLAUDE.md "Idea-to-release pipeline"):
   run /boardroom on it. Update the idea file status and append the board
   verdict + transcript link.
4. PURSUE -> tell the CEO the next step is /discover <project> <idea-file>.
   PARK/PIVOT -> update status, one-line reason in the idea file.
Never let an idea sit in `new` for more than a week without flagging it.
