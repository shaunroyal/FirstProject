# Work folders

Each issue gets a folder, `docs/work/<issue-id>/`, which holds the working record for the
AI-assisted workflow. Use the issue tracker's ID as `<issue-id>`, for example `123` or `PROJ-123`.

| File | Written by | Purpose |
| --- | --- | --- |
| `issue.md` | `/summarise-issue` | Restated issue, assumptions, unknowns, acceptance criteria |
| `plan.md` | `/plan-work` | Numbered steps, files, tests, risks, constitution check. Starts as `Status: Draft` |
| `review.md` | `/review` | Severity-ranked findings and the developer's decisions |
| `debug.md` | `/debug` | Reproduction, hypotheses and proposed fix |

## Rules

- Only the developer changes a plan to `Status: Approved`. `/develop` refuses to start without it.
- Commit work folders with the change. They are the audit trail reviewers read with the PR.
- Never put secrets, real customer data or internal-only URLs in work files.
- To delete old work folders, follow the project's retention rule in `AGENTS.md`. If it has none, keep them.
