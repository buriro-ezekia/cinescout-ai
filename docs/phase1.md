# Phase 1 — Minimal vertical slice

Phase 1 deliberately uses one ADK agent rather than a multi-agent network. Its purpose is to demonstrate the complete technical dependency chain before the specialist workflow becomes the default runtime.

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

A vertical slice reduces integration risk. It proves that Gemini can call the required partner service at runtime and that the resulting evidence reaches the final user-facing response. The Phase 2 specialist workflow is now implemented separately on top of this foundation, without changing the validated Phase 1 entry point.

## Current validation status

The local Phase 1 baseline has been reproduced successfully with Python 3.12, Google ADK 2.7.1 and MCP Python SDK 1.29.0. Dependency integrity, compilation, Ruff, the automated test suite and the repository contract all pass locally.

The repository also includes deterministic pre-credit evaluation contracts that make no Gemini request and no external search request. These checks protect the expected research categories, evidence vocabulary and final response structure while Google Cloud hackathon credits are pending.

## Completion boundary

Phase 1 is complete only when both conditions below are satisfied:

1. the repository contract, offline evaluation contract and automated tests pass; and
2. a credentialled local run demonstrates a real Gemini request that invokes Parallel Search MCP and uses the returned evidence in the final response.

The second condition remains intentionally deferred until a dedicated Google Cloud project can use the hackathon credits. CI must not consume cloud credentials, model quota or partner-service search quota.
