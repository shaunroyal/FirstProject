---
name: API security
description: Security rules for API endpoints and middleware covering authentication, authorisation, validation, rate limits and data exposure.
applyTo: "**/api/**,**/routes/**,**/handlers/**,**/controllers/**,**/endpoints/**,**/middleware/**"
---

# API security

- Every endpoint requires authentication unless it's explicitly listed as public in `docs/architecture.md`.
- Check authorisation per resource (object-level), not just per route. Never trust IDs from the client without an ownership check.
- Validate every request body, query and header against a schema. Reject unknown fields on writes.
- Return only the fields the caller needs. Never serialise internal models straight into responses.
- Apply rate limits and request size limits at the edge or in middleware.
- Configure CORS with explicit origins. Never use `*` with credentials.
- Never log request or response bodies, tokens or personal data. Log a request ID instead.
- Verify webhook and service-to-service calls (signatures or mTLS, following the platform standard).
