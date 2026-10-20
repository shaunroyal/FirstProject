---
name: Python testing
description: Rules for writing pytest tests for Python code and data transformations.
applyTo: "**/test_*.py,**/*_test.py,**/tests/**/*.py,**/conftest.py"
---

# Python testing

- Use `pytest`. Name tests `test_<behaviour>_<condition>`.
- Reuse fixtures from `conftest.py` before creating new setup helpers.
- Use `pytest.mark.parametrize` for input and output tables instead of copy-pasted tests.
- Build small synthetic DataFrames or records inline. Never load production extracts.
- Mock external services (cloud storage, warehouses, APIs) at the client boundary. Unit tests make no network calls.
- Use `tmp_path` for files, and fix seeds and clocks for determinism.
- Assert on values and schema (columns and dtypes) for transformations, not just row counts.
