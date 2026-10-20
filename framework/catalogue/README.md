# Stack catalogue

Each folder is a **stack layer**: a set of scoped Copilot instruction files.
`/start-project` copies `generic` and every chosen stack into the project's
`.github/instructions/catalogue/<stack>/`. `/sync-framework` keeps those copies up to date.

| Stack | Use when |
| --- | --- |
| [generic](generic/) | Always installed |
| [python-dbt](python-dbt/) | Python and dbt data pipelines and transformations |
| [terraform](terraform/) | Infrastructure as code with Terraform |
| [api-service](api-service/) | HTTP or REST APIs and backend services, any language |

## Add a stack

1. Create `framework/catalogue/<stack>/`. Use lowercase letters, digits and hyphens for the name.
2. Add a `README.md` with a `# <stack>` heading, a line `Use when: <one sentence>` and a table of its files. `/start-project` reads it to offer the stack.
3. Add one or more `<topic>.instructions.md` files. Each needs frontmatter with:
   - `description`: what it covers and when it applies (used for on-demand loading)
   - `applyTo`: a glob relative to the workspace root. Separate several globs with commas.
4. Keep each file short: under about 40 lines of rules. Give the reason for any rule that isn't obvious. Skip anything a linter or formatter already enforces.
5. Add a row to the table above and a line to `CHANGELOG.md` (a new stack is a minor version change).
6. Run `sh framework/scripts/check-framework.sh`. Then test the stack on a sample repo, as described in `docs/framework/GOVERNANCE.md`.

## Writing rules

- One topic per file: style, testing, security or pitfalls.
- Write in the imperative: "Use …", "Never …".
- No project names, internal URLs, secrets or customer data.
