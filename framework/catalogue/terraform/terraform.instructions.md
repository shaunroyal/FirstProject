---
name: Terraform style
description: Terraform coding rules covering layout, naming, variables, providers and state.
applyTo: "**/*.tf"
---

# Terraform style

- Run the format and validate commands from `AGENTS.md` after every change.
- File layout: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf` (required versions and providers), and `locals.tf` if needed.
- Use `snake_case` for all names. Don't repeat the resource type in its name (`google_storage_bucket.raw`, not `google_storage_bucket.raw_bucket`).
- Every variable has a `type` and a `description`, plus `validation` where values are constrained. Mark sensitive variables `sensitive = true`.
- Every output has a `description`.
- Pin the Terraform version and provider versions with `~>` constraints in `versions.tf`.
- Use remote state with locking, as `AGENTS.md` describes. Never commit `.tfstate` files or `.terraform/`.
- Prefer `for_each` over `count` for collections, so that removing one item doesn't recreate the others.
- Apply consistent labels or tags (owner, environment, cost centre) through a shared `locals` map.
- Never hard-code project IDs, account IDs or regions in resources. Pass them as variables.
