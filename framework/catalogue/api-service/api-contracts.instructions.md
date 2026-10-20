---
name: API contracts
description: Rules for OpenAPI or Swagger specifications and API contract changes.
applyTo: "**/openapi*.yaml,**/openapi*.yml,**/openapi*.json,**/swagger*.yaml,**/swagger*.yml,**/swagger*.json"
---

# API contracts

- The spec is the contract. Update it in the same change as the code.
- Describe every operation with `operationId`, `summary`, request schema, response schemas (including errors) and security requirements.
- Reuse shared schemas through `components`. Don't inline duplicates.
- Mark required fields explicitly, and give field formats (`date-time`, `uuid`, `email`).
- Use synthetic examples only.
- Breaking changes (removing or renaming a field, a new required input, a type change) need a new version and an ADR.
