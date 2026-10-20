---
name: Terraform safety
description: Safety rules for Terraform changes covering plan before apply, credentials, destructive changes and IAM.
applyTo: "**/*.tf,**/*.tfvars,**/*.tfvars.json"
---

# Terraform safety

- **Plan before apply.** Never run `terraform apply` or `destroy`. Run `terraform plan` only if `AGENTS.md` lists it, and show the developer the plan summary.
- Applies happen through Harness, not from a workstation, unless `AGENTS.md` says otherwise.
- **No hard-coded credentials.** No keys, passwords or tokens in `.tf` or `.tfvars`. Use workload identity or the secret store named in `AGENTS.md`.
- Don't commit `.tfvars` files that contain environment-specific secrets. Keep example values in `*.tfvars.example`.
- Flag any change whose plan would **replace or destroy** a stateful resource (databases, buckets, disks), and ask before proceeding.
- Add `lifecycle { prevent_destroy = true }` to critical stateful resources.
- Grant IAM at the narrowest scope, using predefined or custom roles. Never grant owner or editor roles, and never grant to `allUsers` or `allAuthenticatedUsers` without explicit approval.
- Enable encryption, logging and private networking by default. Public exposure needs an ADR.
