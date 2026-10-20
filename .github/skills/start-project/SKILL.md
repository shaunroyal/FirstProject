---
name: start-project
description: Interview the developer one phase at a time and generate this repo's project context files (AGENTS.md, README, constitution, architecture, scoped instructions, CODEOWNERS, .ai-framework.yml). Use once, right after creating a repo from the template.
argument-hint: "[optional: phase number to redo, e.g. 3]"
disable-model-invocation: true
---

# /start-project

Turn this repo from the template into a configured project. You interview; the developer decides. Run in Agent mode, because you need to edit files.

## Before you start

1. Read [framework/WORKFLOW.md](../../../framework/WORKFLOW.md) sections 5 and 6, plus `.ai-framework.yml`, `README.md`, `AGENTS.md`, `docs/constitution.md` and `docs/architecture.md`.
2. If the `origin` remote URL matches `template_repo` in `.ai-framework.yml`, stop. Explain that this is the template repo itself and `/start-project` runs only in repos created from it.
3. If `template_mode` is `false`, the project is already set up. Ask which phases to redo, and keep all other content as it is.
4. List the folders in `framework/catalogue/`. Read each one's `README.md` to learn which stacks exist and when to use them.
5. Read any project content in `README.md` outside the `template-only` markers. Pre-fill answers from it, and ask only what it doesn't answer.

## Interview rules

- One phase at a time. Ask the phase's questions in one short message.
- After each answer, write a summary of what you understood as a short list. Ask "Correct?" and wait for a yes before moving on.
- "unknown" and "skip" are valid answers. Record them as open questions. Never invent an answer.
- **Never ask for secret values** (passwords, tokens, keys, connection strings). Ask only *where* secrets and config live. If the developer pastes a secret, tell them not to, and don't repeat it or write it anywhere.
- Keep questions concrete. Offer examples, but don't push the developer towards them.

## Phases

1. **Purpose:** the problem it solves, the users, what is out of scope.
2. **Type and stack:** the type (data/ML pipeline, infrastructure, API/service, library, other); languages, frameworks, package manager, runtime versions. Then propose which catalogue stacks to install (`generic` always, plus matches) and confirm.
3. **Commands:** exact commands for install, build, run locally, lint, format, unit test, integration test. "n/a" is fine.
4. **Environments and delivery:** environments; how Harness builds and deploys; where config and secrets live (location only).
5. **Data and risk:** customer or regulated data; data classes; what must never appear in prompts, logs or fixtures.
6. **Architecture:** components; external systems and how they authenticate (method only); platform standards to follow (for example approved GCP services).
7. **Conventions:** branching, commit style, PR size, review rules, code style, test and coverage expectations.
8. **Boundaries:** what agents should *always* do, do only after *asking first*, and *never* do. Suggest these defaults: never edit `.harness/`, never run destructive commands, never commit secrets.
9. **Definition of done:** required checks, docs and sign-offs.
10. **Team:** owners and reviewers (GitHub handles or teams, for CODEOWNERS); where issues and decisions are tracked.

## Preview gate

When all phases are confirmed, list every file you will create, replace or delete, with a full preview of each one's new content. Copied catalogue files can be listed by path only. Then ask: **"Write these files? (yes / change …)"**. Write nothing until the developer says yes.

## Write

After approval:

1. **`AGENTS.md`:** fill every section. Put each unknown under **Open questions** as a question with a suggested owner. Remove every `<FILL:` token.
2. **`README.md`:** delete everything from `<!-- template-only:start -->` to `<!-- template-only:end -->`, including the markers. Fill the project section.
3. **`docs/constitution.md`** and **`docs/architecture.md`:** fill them from phases 1, 5, 6, 7 and 9. Keep the framework's default principles and gates unless the developer removed them.
4. **Catalogue:** for `generic` and each chosen stack, copy `framework/catalogue/<stack>/*.instructions.md` to `.github/instructions/catalogue/<stack>/` without changes.
5. **Project instructions:** if phase 7 or 8 produced rules that the catalogue doesn't cover, write them to `.github/instructions/project/<topic>.instructions.md`, each with `description` and an `applyTo` glob.
6. **`.github/CODEOWNERS`:** owners from phase 10. Keep the framework-owned paths section and assign it to the project owners.
7. **`.github/pull_request_template.md`:** replace the **Definition of done** list with the phase 9 list.
8. **`CHANGELOG.md`:** replace it with an empty Keep a Changelog file for this project, containing only `## [Unreleased]`.
9. **`.ai-framework.yml`:** set `template_mode: false`, `created_from: <template_repo>@v<framework_version>`, `created_on: <today, YYYY-MM-DD>` and `stacks: [...]`. Record confirmed answers under `interview:`, one key per phase, with unknowns in `interview.open_questions`. Leave `framework_version`, `template_repo` and `ownership` unchanged.

## Finish

1. Run `sh framework/scripts/check-framework.sh` and show the result. Fix any `<FILL:` tokens it finds by asking the developer, not by guessing.
2. Summarise: files written, stacks installed, open questions, and the next step ("commit these files on a branch and open a PR").
