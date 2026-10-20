---
name: API testing
description: Rules for testing API endpoints, including contract, error-path and auth tests.
applyTo: "**/test/**,**/tests/**,**/__tests__/**,**/*_test.*,**/*.test.*,**/*.spec.*,**/test_*.*"
---

# API testing

- For each endpoint, test success, validation failure, not found, unauthenticated (`401`) and forbidden (`403`).
- Test object-level authorisation: user A can't read or change user B's resource.
- Assert on status code, response schema and key fields, not on whole response snapshots.
- Use the framework's in-process test client for handler tests. Mock downstream services at the client boundary.
- Keep contract tests that check responses against the OpenAPI spec, if the project has one.
- Integration tests use dedicated test resources and synthetic data, never shared or production environments.
