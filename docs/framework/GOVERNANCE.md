# Framework governance

How the AI-assisted repo framework is owned, changed, versioned and released.

## Owners

| Role | Person | Responsibilities |
| --- | --- | --- |
| Engineering Lead | <FILL: name, @handle> | Technical quality of skills, catalogue, scripts and the Harness template |
| Technical PO | <FILL: name, @handle> | Priorities, triage, release decisions and communication to teams |
| Deputies (optional) | <FILL: names, @handles, or "none"> | Second approver when an owner is the PR author |

The owners jointly own every framework-owned path listed in `.ai-framework.yml` (`ownership.framework_owned`), plus this governance doc.

## Changing the framework

1. **Raise an issue** using the *Framework change* template (label `framework-change`).
2. **Open a PR** against the template repo's default branch. Direct pushes are blocked.
3. The PR must include:
   - [ ] A **before and after example** for any change to a skill, agent or instruction file: what Copilot did before, and what it does after, using the same input. Paste or summarise the transcripts.
   - [ ] **Sample repo results:** the change tested on at least one sample repo per affected stack. A change to `generic`, a skill or an agent affects all supported stacks. See [Sample repos](#sample-repos).
   - [ ] A `CHANGELOG.md` entry under `[Unreleased]`, with the proposed version bump.
   - [ ] A passing `sh framework/scripts/check-framework.sh`.
   - [ ] No secrets, internal URLs or customer data in any file.
4. **Both owners approve.** If an owner is the author, the other owner and a deputy approve.
5. A framework owner merges and releases (see [Releasing](#releasing)).

### Enforcing "both owners approve"

GitHub CODEOWNERS accepts any **one** code owner's approval, so also configure a branch
ruleset on the template repo's default branch:

- Require a pull request before merging, with **2 required approvals**
- Require review from Code Owners
- Dismiss stale approvals when new commits are pushed
- Require status checks: the Harness pipeline that runs the framework check (Harness reports it to GitHub as a commit status)
- Block force pushes and deletions
- Give **write access** to the template repo only to the owners and deputies. Other contributors propose changes from forks.

Because only owners and deputies can approve, two approvals means both owners, or one owner plus a deputy when the other owner is the author.

## Versioning

The framework uses [Semantic Versioning](https://semver.org/). Releases are git tags `vMAJOR.MINOR.PATCH`.

| Bump | When | Examples |
| --- | --- | --- |
| **Major** | Projects must act when they sync | Removing or renaming a skill; changing a gate; changing the `.ai-framework.yml` schema or ownership lists; changing the meaning of `<FILL:` |
| **Minor** | Behaviour changes, backwards compatible | A new skill, stack or check; a rule that changes what Copilot does; a new warning |
| **Patch** | Wording only, no behaviour change | Typos, clearer phrasing, doc fixes |

When in doubt, choose the higher bump.

## Releasing

1. Move `[Unreleased]` entries in `CHANGELOG.md` to a new version heading with today's date.
2. Set `framework_version` in `.ai-framework.yml` to the new version.
3. In `.harness/framework-check.yaml`, bump `versionLabel` and the `FRAMEWORK_LATEST` default, then update the template in Harness.
4. Merge, then tag the merge commit `vX.Y.Z` and create a GitHub release from the changelog entry.
5. Tell teams about the release. For major versions, include the actions projects must take.

## Sample repos

Keep one sample repo per supported stack, created from the template and kept out of production:

| Stack | Sample repo |
| --- | --- |
| generic only | <FILL: repo URL> |
| python-dbt | <FILL: repo URL> |
| terraform | <FILL: repo URL> |
| api-service | <FILL: repo URL> |

To test a change: point the sample repo's `framework` remote at the PR branch, run `/sync-framework`
(or re-run `/start-project` on a fresh copy), then run the standard flow on the sample issue
(`/summarise-issue` through `/pr-description`). Record what you saw in the PR.

## Monthly triage

On the first working week of each month, the owners:

1. Review open `framework-change` issues: accept, decline (with a reason) or ask for more detail.
2. Prioritise accepted issues and plan the next release.
3. Check the VS Code, Copilot and Harness release notes for changes that affect `docs/framework/ASSUMPTIONS.md`, and re-verify those assumptions.
4. Review version drift across project repos (Harness framework-check warnings), and contact teams that are more than two minor versions behind.

## New Copilot capabilities

New Copilot capabilities must be approved through the organisation's **existing tool approval process** before they appear in the template. This covers MCP servers, extensions, new tool sets, hooks, models, and new harnesses or cloud agents. Record the approval reference in `docs/framework/DECISIONS.md`.

## Content rules

Template files must never contain:

- secrets, credentials, tokens or keys, even as examples
- internal hostnames, internal URLs or IP addresses
- customer data, personal data or real production identifiers
- project-specific details in skills (skills read project context at runtime)

`check-framework.sh` scans for common secret patterns, but reviewers remain responsible.

## Drift policy

Projects should stay within **two minor versions** of the latest release. The Harness framework check
warns beyond that. The owners may switch it to strict mode (`FRAMEWORK_STRICT=true`) for a
given org or project after giving notice.
