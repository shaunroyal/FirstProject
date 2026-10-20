---
name: test
description: Add or improve tests for an issue or a set of files, run the project's test commands, and report the results. Use after /develop, or to close test gaps.
argument-hint: "<issue-id | file or folder>"
disable-model-invocation: true
---

# /test

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, and, for an issue, every file in `docs/work/<issue-id>/`.

## Steps

1. Work out the scope: the issue's changed files (`git diff` against the base branch) and acceptance criteria, or the files the developer named.
2. List test gaps: acceptance criteria with no test, untested branches and error paths, and edge cases (empty, null, boundary, invalid input).
3. Write or improve tests for those gaps. Follow the scoped test instructions in `.github/instructions/`. Use synthetic data only.
4. Don't change production code. If a test exposes a bug, leave the test failing, report it, and suggest `/debug`.
5. Run the unit test command from `AGENTS.md`, and the integration test command if the change needs it and `AGENTS.md` lists one.

## Report

- **Tests added or changed:** <file: what each one covers>
- **Commands run:** <command → pass/fail counts>
- **Failures:** <test, likely cause, whether it's a bug or a test problem>
- **Remaining gaps:** <what still isn't covered, and why>
