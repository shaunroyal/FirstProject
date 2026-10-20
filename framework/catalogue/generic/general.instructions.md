---
name: General coding rules
description: Baseline coding rules for every file in the repo, covering scope, structure, errors, logging and dependencies.
applyTo: "**"
---

# General coding rules

- Change only what the approved plan step needs. Unrelated refactors belong in a separate plan.
- Match the surrounding code's style, naming and structure before inventing new patterns.
- Prefer clear code to clever code. Add a comment only to explain *why*, not *what*.
- Keep functions small and focused. Pass dependencies in rather than reaching for globals, so the code stays testable.
- Handle errors explicitly. Never swallow an exception silently. Give the error enough context to act on, without sensitive values.
- Log events and identifiers, not payloads. Never log secrets, tokens or personal data.
- Don't add a dependency without asking first. Pin versions the way the project's package manager expects.
- Delete dead code instead of commenting it out. Version control keeps the history.
- Never leave `TODO`s without an issue reference.
