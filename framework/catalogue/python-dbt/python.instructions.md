---
name: Python style
description: Python coding rules covering typing, structure, errors, logging and data handling.
applyTo: "**/*.py"
---

# Python style

- Target the Python version in `AGENTS.md`. Use the project's formatter and linter rather than hand-formatting.
- Add type hints to all public functions. Avoid `Any` unless you give a reason.
- Use `pathlib` for paths, f-strings for formatting, and `dataclasses` or Pydantic models for structured data.
- Use the `logging` module, not `print`. Log identifiers and counts, never rows or personal data.
- Catch specific exceptions. Never use a bare `except:` or `except Exception: pass`.
- Don't use mutable default arguments.
- Read configuration from the environment or config files named in `AGENTS.md`, never from literals.
- For data work, prefer vectorised operations over row loops. Stream or chunk large inputs instead of loading everything into memory.
- Manage dependencies only with the package manager in `AGENTS.md`, and ask before adding one.
