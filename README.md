<!-- template-only:start -->
<!-- markdownlint-disable-file MD025 -->
# AI-assisted repo template

A GitHub template for starting new repos that use **GitHub Copilot in VS Code**,
with **Harness** for CI/CD. It gives every repo:

- generic Copilot slash commands (Agent Skills) for the whole dev workflow
- `/start-project`, an interview that writes this repo's project context files
- human gates: plan approval before code, review of each step, approval before fixes
- a validation script and a reusable Harness step template

## Start a new repo

1. On GitHub, select **Use this template** → **Create a new repository**.
2. Clone it and open it in VS Code with GitHub Copilot enabled.
3. In Copilot Chat, type `/start-project` and answer the questions.

Full guide: [docs/framework/GUIDE.md](docs/framework/GUIDE.md).
Owners and change process: [docs/framework/GOVERNANCE.md](docs/framework/GOVERNANCE.md).

`/start-project` deletes this section and writes the project README below.
<!-- template-only:end -->

# <FILL: project name>

<FILL: one-paragraph description of what this repo does and for whom>

## Getting started

<FILL: prerequisites and install, run and test commands (mirrors AGENTS.md)>

## Documentation

- [AGENTS.md](AGENTS.md): project context for people and AI agents
- [docs/constitution.md](docs/constitution.md): principles and quality gates
- [docs/architecture.md](docs/architecture.md): components and integrations
- [docs/decisions/](docs/decisions/): architecture decision records
- [docs/framework/GUIDE.md](docs/framework/GUIDE.md): how to use the AI workflow
