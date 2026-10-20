---
name: dbt models
description: Rules for writing dbt SQL models covering layering, naming, references and SQL style.
applyTo: "**/models/**/*.sql,**/macros/**/*.sql,**/snapshots/**/*.sql"
---

# dbt models

- Follow the layers: `staging` (one model per source table, renaming and casting only), then `intermediate`, then `marts` (business-facing).
- Name models by layer: `stg_<source>__<entity>`, `int_<entity>_<verb>`, and `fct_<event>` or `dim_<entity>` in marts.
- Reference models with `{{ ref() }}` and sources with `{{ source() }}`. Never hard-code database or schema names.
- **No `select *` in marts.** List the columns explicitly so schema changes are deliberate.
- Put CTEs at the top: import CTEs first, then logical CTEs, then a final `select`.
- Give every model a clear grain, one row per X, and state it in the model's YAML description.
- Use `incremental` materialisation only with a tested `unique_key` and a documented late-arriving data strategy.
- Use macros only for logic you would otherwise repeat. Don't hide simple SQL in them.
- Never filter or join on personal data columns unless the data rules in `AGENTS.md` allow it.
