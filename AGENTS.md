# AGENTS.md

Project context for AI agents (GitHub Copilot in VS Code) and for people.
Every framework skill reads this file first. Keep it accurate and short.

> Filled in by `/start-project`. Tokens like `<FILL: ...>` mark gaps.
> `framework/scripts/check-framework.sh` fails while any remain.

## Project

- **Name:** <FILL: project name>
- **Purpose:** <FILL: one or two sentences on the problem this repo solves>
- **Users:** <FILL: who uses it>
- **Out of scope:** <FILL: what this repo deliberately does not do>
- **Type:** <FILL: data/ML pipeline | infrastructure | API/service | library | other>

## Stack

- **Languages and versions:** <FILL: e.g. Python 3.12>
- **Frameworks:** <FILL: e.g. dbt-core 1.9>
- **Package manager:** <FILL: e.g. uv>
- **Installed catalogue stacks:** <FILL: e.g. generic, python-dbt>

## Commands

Agents may run **only** the commands in this table. Anything else needs the developer's approval first.

| Purpose | Command |
| --- | --- |
| Install | <FILL: command> |
| Build | <FILL: command or "n/a"> |
| Run locally | <FILL: command or "n/a"> |
| Lint | <FILL: command> |
| Format | <FILL: command> |
| Unit test | <FILL: command> |
| Integration test | <FILL: command or "n/a"> |
| Framework check | `sh framework/scripts/check-framework.sh` |

## Environments and delivery

- **Environments:** <FILL: e.g. dev, test, prod>
- **Delivery:** <FILL: how Harness builds and deploys this repo>
- **Config and secrets live in:** <FILL: location only, never values>

## Data and risk

- **Data handled:** <FILL: data classes, e.g. customer PII, internal, public>
- **Regulated data:** <FILL: yes/no and which regime>
- **Must never appear in prompts, logs or test fixtures:** <FILL: list>
- Use synthetic data in tests and examples. Never paste real records into chat.

## Architecture

See [docs/architecture.md](docs/architecture.md). Platform standards: <FILL: e.g. GCP services and internal standards to follow>

## Conventions

- **Branching:** <FILL: e.g. short-lived feature branches from main>
- **Commits:** <FILL: e.g. Conventional Commits>
- **PR size:** <FILL: e.g. under 400 changed lines>
- **Review rules:** <FILL: e.g. one approval from CODEOWNERS>
- **Code style:** <FILL: formatter and linter, plus anything they don't enforce>
- **Tests and coverage:** <FILL: expectations>

## Boundaries

- **Always:** <FILL: e.g. run lint and unit tests before declaring a step done>
- **Ask first:** <FILL: e.g. adding a dependency, changing a public interface, schema changes>
- **Never:** <FILL: e.g. edit .harness/, run destructive commands, commit secrets>

## Definition of done

<FILL: required checks, docs and sign-offs. /start-project writes the full list here.>

## Team

- **Owners:** <FILL: names or GitHub handles>
- **Reviewers:** <FILL: names, teams or GitHub handles>
- **Issues tracked in:** <FILL: e.g. GitHub Issues, Jira project KEY>
- **Decisions tracked in:** [docs/decisions/](docs/decisions/)

## AI workflow

This repo uses the AI-assisted repo framework. Workflow rules for every skill live in
[framework/WORKFLOW.md](framework/WORKFLOW.md). Typical flow:
`/summarise-issue` → `/plan-work` → (approve plan) → `/develop` → `/test` → `/review` → `/pr-description`.

## Open questions

<!-- /start-project lists unanswered interview questions here. Remove items as they are resolved. -->
- None yet.
