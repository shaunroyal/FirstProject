---
name: dbt tests and docs
description: Rules for dbt YAML files covering model tests, documentation, sources and project config.
applyTo: "**/models/**/*.yml,**/models/**/*.yaml,**/dbt_project.yml,**/sources.yml"
---

# dbt tests and docs

- Every model has a YAML entry with a `description`, including its grain.
- Every primary key column has `unique` and `not_null` tests. Composite keys use a uniqueness test on the combined key.
- Foreign keys have `relationships` tests. Status-type columns have `accepted_values` tests.
- Declare sources with `freshness` checks where the data is time-sensitive.
- Mark personal or sensitive columns with `meta` tags that match the data classes in `AGENTS.md`.
- Set materialisation defaults by folder in `dbt_project.yml`, and override per model only with a reason.
- Never put credentials in `profiles.yml` in the repo. Use environment variables or the secret store named in `AGENTS.md`.
