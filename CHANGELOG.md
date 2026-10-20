# Changelog

All notable changes to this framework are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html) as defined in
[docs/framework/GOVERNANCE.md](docs/framework/GOVERNANCE.md).

## [Unreleased]

## [0.1.0] - 2026-10-20

### Added

- Project context skeletons: `AGENTS.md`, `README.md`, `.ai-framework.yml`, constitution, architecture, ADR template.
- `/start-project` interview skill that generates project context files.
- Workflow skills: `/summarise-issue`, `/plan-work`, `/develop`, `/test`, `/review`, `/debug`, `/pr-description`, `/update-docs`, `/sync-framework`.
- Read-only `planner` and `reviewer` custom agents.
- Stack catalogue: `generic`, `python-dbt`, `terraform`, `api-service`.
- Governance docs, CODEOWNERS, PR and issue templates.
- `framework/scripts/check-framework.sh` and a reusable Harness step template.
- Engineer guide (`docs/framework/GUIDE.md`) and markdownlint config.

[Unreleased]: <FILL: template repo URL>/compare/v0.1.0...HEAD
[0.1.0]: <FILL: template repo URL>/releases/tag/v0.1.0
