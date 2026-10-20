---
name: Testing baseline
description: Rules for writing and changing automated tests in any language.
applyTo: "**/test/**,**/tests/**,**/__tests__/**,**/spec/**,**/*_test.*,**/*.test.*,**/*.spec.*,**/test_*.*"
---

# Testing baseline

- Every behaviour change needs a test that fails without the change.
- Name each test after the behaviour it checks, for example `returns_404_when_order_missing`.
- Use Arrange, Act, Assert, with one behaviour per test.
- Cover the happy path, edge cases (empty, null, boundary values) and error paths.
- Keep unit tests fast and deterministic: no network, no real clock, no shared state. Use fakes or mocks at the boundaries.
- Use synthetic test data. Never copy production records into fixtures.
- Don't weaken, skip or delete a failing test to make a build pass. Report it instead.
- Test public behaviour, not private implementation details.
