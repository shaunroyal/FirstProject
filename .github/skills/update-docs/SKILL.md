---
name: update-docs
description: Bring README.md, AGENTS.md, docs/architecture.md and ADRs in line with what the current change actually did. Use before opening a PR.
argument-hint: "<issue-id>"
disable-model-invocation: true
---

# /update-docs

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, `docs/architecture.md`, `docs/decisions/`, every file in `docs/work/<issue-id>/`, and the `ownership` lists in `.ai-framework.yml`.

## Rules

- Document what the diff shows, not what was planned.
- Edit only project-owned docs. Never edit files listed under `ownership.framework_owned`.
- Change `docs/constitution.md` and the **Boundaries** section of `AGENTS.md` only if the developer explicitly asks. Otherwise, propose the change in your reply.
- Keep edits minimal, and match the existing style.

## Steps

1. Read the diff (`git diff <base>...HEAD` and the working tree).
2. Check each target and update it where the change affects it:
   - `README.md`: setup, usage, commands.
   - `AGENTS.md`: commands, stack, environments, data rules, conventions. Remove **Open questions** the change answered.
   - `docs/architecture.md`: components, external systems, data flow.
   - `docs/decisions/`: if the change made a significant or hard-to-reverse decision, draft a new ADR from `0000-template.md` with the next free number and `Status: Proposed`.
3. If the change adds a command, check it's in the AGENTS.md **Commands** table.

## Finish

List each file you changed, with a one-line reason, plus any changes you are only proposing. Ask the developer to review the diff and keep or undo each edit.
