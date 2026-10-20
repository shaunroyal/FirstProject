---
name: API design
description: REST and HTTP API design rules covering resources, status codes, errors, pagination and versioning. Use when creating or changing API endpoints.
applyTo: "**/api/**,**/routes/**,**/handlers/**,**/controllers/**,**/endpoints/**"
---

# API design

- Keep handlers thin: parse and validate, call a service function, then map the result to a response. Business logic lives in the service layer.
- Use plural nouns for resources (`/orders/{id}`) and HTTP verbs for actions. Avoid verbs in paths.
- Return the right status codes: `201` with a `Location` header on create, `204` for no content, `400` or `422` for invalid input, `404` for missing, and `409` for conflicts.
- Return errors in one consistent format (for example RFC 9457 problem details), with no stack traces or internal details.
- Paginate every list endpoint, with a maximum page size.
- Make `PUT` and `DELETE` idempotent. Support idempotency keys on `POST` where retries can create duplicates.
- Version the API (in the path or a header, following the project convention). Never make a breaking change to a published version.
- Use one convention for timestamps (ISO 8601, UTC) and one casing style for field names across the API.
