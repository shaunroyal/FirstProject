---
name: debug
description: Reproduce a bug, rank hypotheses with evidence, and propose a minimal fix with a regression test. Applies the fix only after the developer approves it.
argument-hint: "<issue-id> <symptom, error message or failing test>"
disable-model-invocation: true
---

# /debug

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, and every file in `docs/work/<issue-id>/`.

If there is no `<issue-id>`, ask for one. If the developer has none, keep notes in chat and don't write `debug.md`.

## Steps

1. **Reproduce.** Find the smallest reliable way to trigger the bug using commands from `AGENTS.md`, for example a single failing test. If you can't run it, give the developer exact steps to run and wait for the output.
2. **Hypothesise.** List up to three likely causes, ranked, each with the evidence for and against.
3. **Narrow.** Check hypotheses by reading code, adding temporary logging, or running allowed commands. Use no real data. Remove temporary logging afterwards.
4. **Propose.** Show the minimal fix as a diff, plus a regression test that fails before the fix and passes after it. Name any side effects.
5. **Gate.** Ask: **"Apply this fix? (yes / no / change …)"**. Change nothing in production code before a yes.
6. **Apply.** After a yes, apply the fix and the test, run the unit test command, and report the result.

If the fix is bigger than a few lines, or it changes behaviour beyond the bug, don't apply it. Suggest `/plan-work` instead.

## Output: `docs/work/<issue-id>/debug.md`

```markdown
# Debug: <issue-id>

## Symptom
## Reproduction
<exact steps or command, plus the observed and expected results>
## Hypotheses
| # | Cause | Evidence | Result |
| --- | --- | --- | --- |
## Root cause
## Fix
Status: Proposed | Approved by <developer> on <date> | Rejected
<summary and files>
## Regression test
<test name and file>
```
