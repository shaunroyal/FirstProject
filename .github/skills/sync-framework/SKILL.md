---
name: sync-framework
description: Compare this repo's framework-owned files with the latest template release, propose updates as a diff, apply them only after approval, and bump framework_version. Never overwrites project-owned files.
argument-hint: "[target version, e.g. 0.3.0; defaults to latest]"
disable-model-invocation: true
---

# /sync-framework

## Before you start

Follow [framework/WORKFLOW.md](../../../framework/WORKFLOW.md). Read `AGENTS.md`, `README.md`, `docs/constitution.md` and `.ai-framework.yml`. From `.ai-framework.yml`, note `framework_version` (call it CURRENT), `template_repo`, `stacks` and both `ownership` lists. Those lists are the only source of what you may change.

If `template_mode` is `true`, stop: this is the template repo itself.

## 1. Fetch the framework

1. Run `git remote -v`. If there's no `framework` remote, ask the developer to approve this, then run it:
   `git remote add framework <template_repo>`
2. Ask the developer to approve this, then fetch framework tags into their own namespace so they can't clash with project tags:
   `git fetch framework --no-tags "+refs/tags/v*:refs/tags/framework/v*"`
3. Set TARGET to the version the developer gave, or else the highest `framework/v*` tag (`git tag -l "framework/v*" --sort=-v:refname`).
4. If TARGET equals CURRENT, report "Up to date" and stop. If the tag `framework/v<CURRENT>` doesn't exist, stop and ask the developer which version this repo really has.

## 2. Work out the changes (read-only)

1. **Release notes:** `git show framework/v<TARGET>:CHANGELOG.md`. Summarise the entries after CURRENT. Call out a major version change as breaking.
2. **Framework-owned files:** for each path in `ownership.framework_owned`, run
   `git diff framework/v<CURRENT> framework/v<TARGET> -- <path>`.
   Map catalogue files: upstream `framework/catalogue/<stack>/` becomes local `.github/instructions/catalogue/<stack>/`, for installed `stacks` only. Mention new upstream stacks, but don't install them.
3. **Local edits:** compare each framework-owned file in the working tree with its `framework/v<CURRENT>` version. If a file was edited locally, flag it. Updating it would drop those edits, so it needs its own approval.
4. **Project-owned files:** run `git diff framework/v<CURRENT> framework/v<TARGET> -- <path>` on the template's versions of these files. Never write them. List upstream changes the team might want to copy by hand, for example a new constitution gate or a new AGENTS.md section.
5. **Ownership changes:** if the `ownership` lists in the upstream `.ai-framework.yml` changed, flag them for manual review.

## 3. Propose (gate)

Show a table with one row per file: `Add | Update | Delete | Skip (locally edited) | Manual review (project-owned)`, plus a one-line reason, and the full diff for each Add, Update or Delete.
Ask: **"Apply these framework updates? (all / list of files / no)"**. Change nothing until you get an answer.

## 4. Apply (approved files only)

1. Write each approved file using the content from `git show framework/v<TARGET>:<upstream path>`. Delete files only if their deletion was approved.
2. In `.ai-framework.yml`, set `framework_version: <TARGET>`. Change nothing else there.
3. Run `sh framework/scripts/check-framework.sh` and show the result.

## Finish

Report what was updated, skipped and flagged for manual review. Suggest committing on a branch called `chore/sync-framework-v<TARGET>` and opening a PR with this report as the description.
