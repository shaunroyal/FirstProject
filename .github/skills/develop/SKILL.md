---
name: develop
description: Implement exactly one step of an approved plan, with tests, then pause for review. Refuses to start unless docs/work/<issue-id>/plan.md has Status Approved.
argument-hint: "<issue-id> [step number]"
disable-model-invocation: true
---

# /develop

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, and every file in `docs/work/<issue-id>/`.

## Gate

Open `docs/work/<issue-id>/plan.md`. Unless it has a line that reads exactly `Status: Approved`, **stop**. Make no changes, and reply:
"The plan isn't approved. Review `plan.md`, set `Status: Approved`, then run `/develop <issue-id>` again."

## Steps

1. Pick the step: the number the developer gave, or else the first unticked `[ ]` step. Say which step you are doing.
2. Implement **only that step**. Touch only the files the step lists. If you need another file, a new dependency, or anything under "Ask first" in `AGENTS.md`, stop and ask.
3. Add or update the step's tests. Follow the scoped instructions in `.github/instructions/`.
4. Run the format, lint and unit test commands from `AGENTS.md`. Fix failures caused by your change. Report any other failures without fixing them.
5. In `plan.md`, tick the step (`[x]`) and add one line under it: `Done: <date>, <summary>, tests: <pass/fail>`.

## If the plan is wrong

If the step can't be done as written, stop. Explain why and propose the change to `plan.md`. Applying it sets `Status: Draft`, and the developer must approve again.

## Pause

End every run with:

- **Step:** `<number and title>`
- **Changed:** `<files>`
- **Commands run:** `<command → result>`
- **Next step:** `<number and title>`, or "all steps done, run `/review <issue-id>`"

Then ask: **"Review the diff. Reply 'next' to continue with the next step."** Never start the next step without that reply.
