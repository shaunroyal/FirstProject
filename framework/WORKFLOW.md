# Framework workflow rules

Shared rules for every framework skill in `.github/skills/`. Framework-owned: change via the template repo only.

## 1. Load context first

Before doing anything else, read:

1. `AGENTS.md`
2. `README.md`
3. `docs/constitution.md`
4. `docs/work/<issue-id>/` (every file that exists) when the skill works on an issue

If `AGENTS.md` still contains `<FILL:` tokens, stop and tell the developer to run `/start-project` first.

## 2. Issue ID

Skills that work on an issue need an `<issue-id>` (for example `123` or `PROJ-123`).
Take it from the developer's message. If it is missing, ask for it. Never guess.
Work files live in `docs/work/<issue-id>/`. See `docs/work/README.md`.

## 3. Commands

- Run only commands listed in the **Commands** table of `AGENTS.md`.
- For anything else, show the exact command and why, then wait for approval.
- Never run destructive commands (deleting data, force-pushing, `terraform apply`, dropping tables) unless `AGENTS.md` explicitly allows it and the developer approves this specific run.

## 4. Human gates

- No code before `docs/work/<issue-id>/plan.md` contains `Status: Approved`. Only the developer sets that line.
- Pause after each plan step for review.
- Propose fixes and framework updates as diffs. Apply them only after explicit approval.
- When a gate is not met, stop and say exactly what is needed.

## 5. Data and secrets

- Never ask for, print or write secret values. Refer only to where they live.
- Follow the **Data and risk** section of `AGENTS.md`. Use synthetic data in tests and examples.

## 6. Honesty

- Mark assumptions as assumptions. List unknowns instead of filling gaps.
- Report command results faithfully, including failures and skipped steps.

## 7. Output

- Be brief. Use the section headings each skill specifies.
- Reference files as relative paths, with line numbers where useful.
