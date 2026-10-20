# Assumptions

Facts about tools and platforms that this framework relies on. Each item was checked
against the source shown, on the date shown. Re-check them when VS Code, Copilot or Harness change.

| # | Assumption | Source and date checked | Impact if wrong |
| --- | --- | --- | --- |
| A1 | VS Code offers several agent **harnesses**. **Copilot** is the recommended default; **Local** is VS Code's built-in harness. | VS Code docs, *Choose an agent harness*, 2026-10-14 | Guide wording |
| A2 | `.prompt.md` prompt files run **only** in the Local harness. The Copilot harness uses **Agent Skills** instead. | VS Code docs, *Prompt files* and *Migrate customizations*, 2026-10-14 | This is why the framework ships skills, not prompt files (see D1) |
| A3 | Project skills live in `.github/skills/<name>/SKILL.md`. Frontmatter: `name` (required, lowercase letters, digits and hyphens, must match the folder, max 64 chars) and `description` (required, max 1024 chars). Optional: `argument-hint`, `user-invocable`, `disable-model-invocation`, `context`. Skills appear as slash commands in both the Copilot and Local harnesses. | VS Code docs, *Agent Skills*, 2026-10-14 | Commands not found. `check-framework.sh` validates the format |
| A4 | `disable-model-invocation: true` stops the agent loading a skill on its own, so it runs only when typed as `/name`. | VS Code docs, *Agent Skills*, 2026-10-14 | Gated skills could run unprompted |
| A5 | The Copilot harness has a built-in `/plan` (Plan agent). | VS Code docs, *Choose an agent harness*, 2026-10-14 | Name clash, so our skill is `/plan-work` (see D2) |
| A6 | `.github/copilot-instructions.md` and root `AGENTS.md` are both read as project instructions. In the Local harness, `chat.useAgentsMdFile` controls AGENTS.md support. | VS Code docs, *Custom instructions*, 2026-10-14 | AGENTS.md ignored; copilot-instructions.md still points to it |
| A7 | Scoped instructions are `*.instructions.md` files under `.github/instructions/`, searched recursively. Frontmatter: `applyTo` (glob from the workspace root), `description`, `name`. | VS Code docs, *Custom instructions*, 2026-10-14 | Catalogue rules not applied |
| A8 | Custom agents are `.github/agents/*.agent.md` with frontmatter `name`, `description` and `tools`. `['read', 'search']` gives read-only access. Chat modes are replaced by custom agents. | VS Code docs, *Custom agent file reference*, 2026-10-16 | Planner and reviewer agents not read-only |
| A9 | Applicable instruction sources are additive, with no guaranteed precedence. | VS Code docs, *Custom instructions*, 2026-10-14 | copilot-instructions.md says AGENTS.md wins, but conflicts must be fixed at source |
| A10 | Harness templates use a top-level `template:` with `name`, `identifier`, `versionLabel`, `type` (`Step`, `Stage`, `StepGroup`, `Pipeline`), optional `orgIdentifier` and `projectIdentifier`, and `spec`. A CI `Run` step takes `connectorRef`, `image`, `shell` and `command`. `<+input>` marks runtime inputs, and `<+input>.default(x)` sets a default. | Harness Developer Hub source (`harness/developer-hub`), 2026-09-29 | Template import fails; adjust in Harness UI |
| A11 | GitHub CODEOWNERS can't require approval from *all* listed owners. Any one code owner's approval satisfies a path. | GitHub docs (known behaviour) | "Both owners approve" needs extra settings (see GOVERNANCE.md) |
| A12 | Engineers run VS Code with GitHub Copilot, and the Copilot agent can read and edit workspace files and run terminal commands, with approval. | Brief | Skills can't write files |

The VS Code docs site was not reachable from the build environment. Its content was read
from the official source repo `microsoft/vscode-docs` (commit of 2026-10-19).
