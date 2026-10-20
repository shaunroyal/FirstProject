---
name: Terraform modules
description: Conventions for writing and consuming reusable Terraform modules.
applyTo: "**/modules/**/*.tf"
---

# Terraform modules

- A module does one thing, such as "a bucket with standard policy", and has a `README.md` listing its inputs, outputs and an example.
- Modules don't configure providers or backends. The calling root module does.
- Expose the smallest useful set of variables, with safe defaults (private, encrypted, logged).
- Source modules from a pinned version (a git tag or a registry version), never a branch.
- Don't use `depends_on` on modules unless an implicit reference is impossible, and comment why.
- Treat changes to a module's inputs or outputs as breaking. Version and document them.
