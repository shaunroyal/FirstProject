# Engineer guide

How to start a repo from the template, work an issue with Copilot, and keep the framework up to date.

## What you get

- **Slash commands** (Agent Skills in `.github/skills/`) for each step of the workflow.
- **Project context** (`AGENTS.md`, `docs/constitution.md`, `docs/architecture.md`) that every command reads, so the commands stay generic.
- **Human gates:** you approve the plan before any code is written, review each step, and approve fixes and framework updates.
- **A framework check** (`framework/scripts/check-framework.sh`) that runs locally and in Harness.

## One-time setup

1. Install VS Code and sign in to GitHub Copilot with your work account.
2. In the Chat view, start a new session. Use the **Copilot** harness (the default) or **Local**; the skills work in both. See [Copilot settings to check](#copilot-settings-to-check).
3. Type `/` in the chat input. You should see the framework commands, such as `/start-project` and `/plan-work`.

## 1. Create the repo

1. Open the template repo on GitHub and select **Use this template** → **Create a new repository**.
2. Clone it and open the folder in VS Code.
3. Create a branch, for example `chore/project-setup`.

## 2. Run `/start-project`

1. Open Copilot Chat, select the **Agent** agent, and type `/start-project`.
2. Answer the ten phases: purpose, stack, commands, environments, data and risk, architecture, conventions, boundaries, definition of done, team. After each phase, Copilot summarises your answers back; correct it or confirm.
3. Say **unknown** when you don't know. It goes under **Open questions**, and nothing is invented.
4. Never paste secret values. Say only where secrets live (for example "GCP Secret Manager").
5. Review the preview of every file, then approve. Copilot writes the files and runs the framework check.
6. Commit, push and open a PR. Your team's code owners review it.

## 3. Add the framework check to Harness

Ask the framework owners for the template reference (for example `org.ai_framework_check`). Then add the step to your CI stage, after the clone:

```yaml
- step:
    name: Framework check
    identifier: framework_check
    template:
      templateRef: org.ai_framework_check
      versionLabel: "0.1.0"
```

Supply the template's runtime inputs (image connector and image) the way your pipelines usually do. See the comments in `.harness/framework-check.yaml`.

To run it locally:

```sh
sh framework/scripts/check-framework.sh
```

## 4. Work an issue

| Step | Command | What happens | Your gate |
| --- | --- | --- | --- |
| 1 | `/summarise-issue 123` (paste the issue or give its URL) | Restates the issue, assumptions, unknowns and acceptance criteria | Confirm it, then it's saved to `docs/work/123/issue.md` |
| 2 | `/plan-work 123` | Writes small numbered steps, files, tests, risks and a constitution check to `plan.md` as `Status: Draft` | Read the plan and change it to `Status: Approved` yourself |
| 3 | `/develop 123` | Implements **one** step with tests, runs lint and tests, ticks the step | Review the diff, then reply `next`. It refuses to start without an approved plan |
| 4 | `/test 123` | Fills test gaps, runs tests, reports | Optional |
| 5 | `/review 123` | Writes severity-ranked findings to `review.md`. Doesn't change code | Decide what to fix, and record it in **Developer decisions** |
| 6 | `/update-docs 123` | Updates the README, AGENTS.md, architecture and ADR drafts to match the change | Review the diff, then keep or undo |
| 7 | `/pr-description 123` | Drafts the PR body from the PR template | Edit it and open the PR yourself |

Other commands:

- `/debug 123 <symptom>`: reproduces the bug, ranks hypotheses and proposes a minimal fix with a regression test. It applies the fix only when you say yes.
- **planner** and **reviewer** agents (agent picker): read-only helpers for exploring a plan or getting a second review. They can't edit files.

Commit `docs/work/<issue-id>/` with your change. Reviewers use it as the audit trail.

## 5. Update the framework

When a new framework version is released (the Harness check warns when you fall more than two minor versions behind):

1. Create a branch, for example `chore/sync-framework`.
2. Run `/sync-framework`. Approve adding the `framework` remote and fetching tags when asked.
3. Review the proposed changes, then approve all of them, some, or none. Framework-owned files are updated. Project-owned files (`AGENTS.md`, `README.md`, constitution, architecture, your own instructions) are never overwritten; Copilot lists upstream changes for you to copy by hand.
4. Open a PR with the sync report.

Which files are which is defined in `.ai-framework.yml` under `ownership`.

## Propose a framework change

Don't edit framework-owned files in your repo. Your changes would be flagged and could be overwritten on the next sync.
Instead, open a **Framework change** issue on the template repo. See [GOVERNANCE.md](GOVERNANCE.md).

## Copilot settings to check

| Setting or policy | Why |
| --- | --- |
| Copilot agent mode allowed by your org's Copilot policy | Skills need the agent to edit files and run commands |
| Copilot harness selected, or Local | Both load skills from `.github/skills/` |
| `chat.useAgentsMdFile` on (Local harness) | Loads `AGENTS.md` automatically |
| `github.copilot.chat.codeGeneration.useInstructionFiles` on (Local harness) | Loads `.github/copilot-instructions.md` |
| `chat.includeApplyingInstructions` on (Local harness) | Applies the `.instructions.md` files that match by `applyTo` |
| Terminal command approval left on | Keeps you in control of every command an agent runs |

## Troubleshooting

- **A command doesn't appear after `/`:** run **Chat: Open Customizations** and check the Skills list. The skill's `name` must match its folder. Run `sh framework/scripts/check-framework.sh`.
- **Rules aren't followed:** expand **References** in the chat response to see which instructions were loaded. Check the file's `applyTo` glob.
- **`/develop` refuses to start:** `plan.md` must contain the exact line `Status: Approved`.
- **The check fails on `<FILL:`:** a project context file still has a gap. Fill it in, or re-run `/start-project` for that phase.
