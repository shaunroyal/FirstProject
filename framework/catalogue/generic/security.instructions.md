---
name: Security baseline
description: Security rules for every file, covering secrets, input handling, data protection and dependencies.
applyTo: "**"
---

# Security baseline

- Never hard-code secrets, keys, tokens, passwords or connection strings. Read them from the secret store or environment named in `AGENTS.md`.
- Never put real customer or regulated data in code, tests, fixtures, logs, comments or prompts. Use synthetic data.
- Treat all external input as untrusted. Validate type, size and format at the boundary.
- Use parameterised queries and safe APIs. Never build SQL, shell commands or file paths by concatenating strings with input.
- Apply least privilege to service accounts, IAM roles, tokens and file permissions.
- Don't disable TLS verification, authentication or security checks, even "temporarily".
- Prefer well-maintained libraries over hand-written crypto, auth or parsing.
- If you spot a vulnerability outside the current task, report it. Don't fix it silently.
