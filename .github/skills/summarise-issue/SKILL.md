---
name: summarise-issue
description: Restate an issue with assumptions, unknowns and testable acceptance criteria, and save it to docs/work/<issue-id>/issue.md. Use at the start of work on an issue.
argument-hint: "<issue-id> [pasted issue text | issue URL]"
disable-model-invocation: true
---

# /summarise-issue

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, and any files already in `docs/work/<issue-id>/`.

## Input

- An `<issue-id>`, plus either pasted issue text or an issue number or URL.
- If you get a number or URL, read the issue with the tools you have. If you can't, ask the developer to paste the text. Don't guess what it says.

## Steps

1. Read the issue. Search the codebase only enough to understand the terms it uses.
2. Draft the summary below in chat. Leave out secrets, personal data and internal URLs that appear in the issue.
3. Ask: **"Is this right? (yes / change …)"**. Revise until the developer confirms.
4. Write the confirmed text to `docs/work/<issue-id>/issue.md`. If the file exists, show a diff and confirm before replacing it.

## Output: `docs/work/<issue-id>/issue.md`

```markdown
# <issue-id>: <short title>

- **Source:** <link or "pasted">
- **Confirmed by developer:** yes, <YYYY-MM-DD>

## Summary
<2–4 sentences, in plain words>

## Acceptance criteria
1. <testable statement>

## Assumptions
- <assumption> (confirm with: <who>)

## Unknowns and questions
- <question> (ask: <who>)

## Out of scope
- <item>

## Data sensitivity
<data classes touched, per AGENTS.md "Data and risk", or "none">
```

## Finish

Tell the developer the next step: `/plan-work <issue-id>`.
