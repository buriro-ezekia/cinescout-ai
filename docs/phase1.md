# Phase 1 — Minimal vertical slice

Phase 1 deliberately uses one ADK agent rather than a multi-agent network. Its purpose is to demonstrate the complete technical dependency chain before additional orchestration is introduced.

## Runtime path

```text
Production brief or screenplay extract
        |
        v
Gemini through Google ADK
        |
        | identifies externally verifiable matters
        v
Parallel Search MCP
        |
        | web_search / web_fetch
        v
Evidence returned to Gemini
        |
        v
Evidence-backed production intelligence response
```

## Why this is the correct first implementation

A vertical slice reduces integration risk. It proves that Gemini can call the required partner service at runtime and that the resulting evidence reaches the final user-facing response. Multi-agent planning, verification and production-risk specialists can then be introduced without changing the underlying partner integration.

## Completion boundary

Phase 1 is complete when the repository contract and automated tests pass and a credentialled local run demonstrates a real Gemini request that invokes Parallel Search MCP. The latter is intentionally a manual smoke test because CI must not consume cloud credentials or external service quotas.
