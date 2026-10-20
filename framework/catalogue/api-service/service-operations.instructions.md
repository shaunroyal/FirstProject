---
name: Service operations
description: Operational rules for services covering configuration, health checks, observability, shutdown and containers.
applyTo: "**/Dockerfile,**/*.dockerfile,**/config/**,**/health*,**/main.*,**/app.*,**/server.*"
---

# Service operations

- Read all configuration from the environment or config named in `AGENTS.md`. Fail fast at startup if required config is missing.
- Expose a liveness check (process is up) and a readiness check (dependencies are reachable), with no auth and no sensitive output.
- Use structured (JSON) logs with a request or trace ID. Emit the metrics required by the platform standard.
- Handle `SIGTERM`: stop accepting requests, finish in-flight work, then exit within the platform's grace period.
- Set timeouts on every outbound call. Retry only idempotent calls, with backoff and a limit.
- Containers: use a pinned, minimal base image, run as a non-root user, use multi-stage builds, and include no secrets in layers.
