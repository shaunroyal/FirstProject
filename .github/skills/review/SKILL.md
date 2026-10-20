---
name: review
description: Review the current change against the constitution, project conventions, security and data rules, and write severity-ranked findings to docs/work/<issue-id>/review.md. Read-only on code; the developer decides which fixes to make.
argument-hint: "<issue-id>"
disable-model-invocation: true
---

# /review

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md`, every file in `docs/work/<issue-id>/`, and the scoped instructions in `.github/instructions/` that apply to the changed files.

## Rules

- Don't edit code or tests. The only file you write is `review.md`.
- Review the full change: `git diff <base>...HEAD` plus uncommitted changes (`git status`, `git diff`).
- Report only real problems, each with a file and line. Don't report something a linter or formatter in `AGENTS.md` already enforces.
- For a second opinion with no write access at all, the developer can switch to the read-only **reviewer** agent.

## Check against

1. **Plan:** are all steps done, and does the diff contain nothing outside the plan?
2. **Acceptance criteria:** is each one met and tested?
3. **Constitution:** principles, quality gates and non-negotiables.
4. **Conventions:** the AGENTS.md conventions and the scoped instructions.
5. **Security:** input validation, authentication and authorisation, injection, secrets, dependency risk, unsafe defaults.
6. **Data:** the AGENTS.md "Data and risk" rules, including real data in tests, fixtures or logs.
7. **Docs:** whether README, AGENTS.md, architecture or an ADR needs updating.

## Output: `docs/work/<issue-id>/review.md`

```markdown
# Review: <issue-id>

- **Base:** <ref>  **Head:** <short sha or "working tree">
- **Verdict:** Ready | Ready after fixes | Not ready

## Findings
| # | Severity | Location | Finding | Rule broken | Suggested fix |
| --- | --- | --- | --- | --- | --- |

Severity: Critical (blocks merge: security, data or correctness), High (must fix before merge), Medium (should fix), Low (consider), Nit (optional).

## Checklist
- [ ] All plan steps done
- [ ] Every acceptance criterion met and tested
- [ ] No constitution violations
- [ ] Docs up to date

## Developer decisions
| # | Fix / Won't fix / Defer | Reason |
| --- | --- | --- |
```

## Finish

Summarise the counts by severity. Ask the developer to fill in **Developer decisions**. Apply no fixes; the developer can ask for them, or run `/develop` for a planned follow-up step.
