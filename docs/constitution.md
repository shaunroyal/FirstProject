# Constitution

The rules this project will not bend. `/plan-work` checks every plan against this file,
and `/review` checks every diff against it. Keep it short. Change it by PR with owner approval.

## Principles

<!-- /start-project fills these from the interview. Keep 3 to 7, each one line with a reason. -->
1. **Humans decide, agents assist.** Plans are approved before code is written, and every change is reviewed by a person.
2. **Small, reversible changes.** Prefer small PRs that are easy to review and roll back.
3. **Tests prove behaviour.** Every behaviour change ships with tests that would fail without it.
4. <FILL: project-specific principle and its reason>

## Quality gates

A change may merge only when:

- [ ] Its plan in `docs/work/<issue-id>/plan.md` is `Status: Approved`
- [ ] Lint, format and unit tests pass (commands in `AGENTS.md`)
- [ ] Harness CI is green, including the framework check
- [ ] Review findings rated High or Critical are fixed
- [ ] <FILL: project-specific gate, e.g. coverage threshold, integration tests, security scan>

## Non-negotiables

- No secrets, credentials or tokens in code, config, logs, prompts or fixtures.
- No real customer or regulated data outside approved systems. Tests use synthetic data.
- No changes to CI/CD configuration (`.harness/`) without owner approval.
- <FILL: project-specific non-negotiable>

## Exceptions

Record any approved exception as an ADR in `docs/decisions/`, with its owner and expiry date.
