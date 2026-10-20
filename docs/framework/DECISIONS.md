# Framework decisions

Decisions made while building the framework. Add new ones at the end, and don't rewrite old ones;
supersede them instead. Project decisions go in `docs/decisions/` (ADRs), not here.

| # | Decision | Why | Date |
| --- | --- | --- | --- |
| D1 | Ship the slash commands as **Agent Skills** (`.github/skills/<name>/SKILL.md`), not `.prompt.md` files. | Prompt files only run in the Local harness, and Copilot is now the default harness (A2). Skills work in both, plus Copilot CLI and the cloud agent. Chosen by the requester. | 2026-10-20 |
| D2 | Name the planning skill `/plan-work`, not `/plan`. | Avoids the built-in `/plan` in the Copilot harness (A5). Chosen by the requester. | 2026-10-20 |
| D3 | Every skill sets `disable-model-invocation: true`. | Gated workflow steps must run only when a developer asks for them. | 2026-10-20 |
| D4 | Shared skill rules live once in `framework/WORKFLOW.md`, and each skill links to it. | Keeps skills short and avoids drift between copies. | 2026-10-20 |
| D5 | Unfilled values use the token `<FILL: description>`. | Easy to grep and hard to confuse with HTML or `<issue-id>` examples. `check-framework.sh` looks for `<FILL:`. | 2026-10-20 |
| D6 | File ownership is defined once, in `.ai-framework.yml` under `ownership`. | Single source for `/sync-framework`, `/update-docs` and the check script. | 2026-10-20 |
| D7 | Catalogue instructions are copied to `.github/instructions/catalogue/<stack>/` (framework-owned). Team rules go in `.github/instructions/project/` (project-owned). | Folders make ownership obvious and keep sync safe. VS Code searches subfolders (A7). | 2026-10-20 |
| D8 | The template ships no active scoped instructions. `/start-project` installs `generic` plus the chosen stacks. | Avoids two copies of the catalogue in the template repo. | 2026-10-20 |
| D9 | `template_mode: true` in `.ai-framework.yml` marks the template repo. `/start-project` sets it to `false`. | Lets the check script skip placeholder checks in the template only. | 2026-10-20 |
| D10 | `CHANGELOG.md` is the framework's changelog in the template. `/start-project` resets it to an empty project changelog. | A project should track its own releases. `/sync-framework` reads the upstream changelog from the framework remote. | 2026-10-20 |
| D11 | The interview records answers in `.ai-framework.yml` under `interview`, and never records secret values. | Required by the brief, and keeps an audit trail of what the context files were built from. | 2026-10-20 |
| D12 | The previous IntelliJ settings files in this repo were removed. | Unrelated to the template. Chosen by the requester; still in git history. | 2026-10-20 |
