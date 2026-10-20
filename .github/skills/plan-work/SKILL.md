---
name: plan-work
description: Write a small, numbered implementation plan for an issue (steps, files, tests, risks, constitution check) to docs/work/<issue-id>/plan.md with Status Draft. Use after /summarise-issue and before any code.
argument-hint: "<issue-id>"
disable-model-invocation: true
---

# /plan-work

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, `docs/architecture.md`, and every file in `docs/work/<issue-id>/`.

If `docs/work/<issue-id>/issue.md` is missing, stop and suggest `/summarise-issue <issue-id>`.

## Rules

- Plan only. Don't edit any file except `plan.md`.
- Research the code by reading it. Run no commands except read-only git.
- Make each step small enough to review in one sitting: one concern, usually under about 100 changed lines, with its own tests.
- Every acceptance criterion in `issue.md` must map to at least one step.
- Always write `Status: Draft`. **Never** write `Status: Approved`; only the developer does that.
- If `plan.md` already exists, show a diff of your changes. If it was `Approved`, tell the developer that saving resets it to `Draft`.

## Output: `docs/work/<issue-id>/plan.md`

```markdown
# Plan: <issue-id> <short title>

Status: Draft
Approved by: <developer fills in>

## Goal
<one sentence>

## Steps
1. [ ] <what changes>
   - Files: <paths>
   - Tests: <tests to add or change>
   - Done when: <observable check>

## Acceptance criteria coverage
| Criterion | Step(s) |
| --- | --- |

## Risks
| Risk | Likelihood | Mitigation |
| --- | --- | --- |

## Constitution check
| Rule (from docs/constitution.md) | OK / Concern | Note |
| --- | --- | --- |

## Needs approval (from AGENTS.md "Ask first")
- <dependency, interface or schema changes, or "none">

## Open questions
- <question>
```

## Finish

Say: **"Review the plan. When you're happy, change `Status: Draft` to `Status: Approved` and run `/develop <issue-id>`."**
