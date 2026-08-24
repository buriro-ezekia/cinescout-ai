# Pre-credit hardening

CineScout AI can continue to make meaningful engineering progress before Google Cloud hackathon credits are available. This work deliberately excludes Gemini and Vertex AI requests so that routine development remains at no cost.

## Purpose

The pre-credit hardening layer prepares the repository for the eventual live Phase 1 acceptance test without weakening the project's evidence requirements or introducing a substitute model. It concentrates on deterministic contracts, controlled evaluation scenarios, dependency integrity and partner-connectivity checks.

## At-no-cost validation boundary

The following checks make no Gemini request and no Parallel search request:

```text
pip check
    |
    v
Python compilation
    |
    v
Ruff
    |
    v
pytest
    |
    v
controlled evaluation corpus
    |
    v
repository contract
```

The controlled corpus in `evals/scenarios.json` covers historical context, cultural context, geography and locations, institutions, props or technology, terminology, logistics and rights context. These scenarios do not attempt to answer the research questions offline. Instead, they define what later live evaluations must recognise and how the final response must be structured.

## Production-research contract

`app/contracts.py` defines the shared research categories, evidence-status vocabulary and required response sections. This provides a stable interface for later specialist agents without introducing multi-agent orchestration before the Phase 1 runtime path has been demonstrated.

The evidence states are:

- `high`;
- `medium`;
- `low`; and
- `insufficient_evidence`.

The required response sections remain:

- Production reading;
- Evidence and verification;
- Production implications;
- Uncertainty or conflicts; and
- Sources consulted.

## Optional Parallel connectivity probe

`scripts/check_parallel_mcp.py` is a manual connectivity check. It connects to the configured Parallel Search MCP endpoint, performs the MCP initialisation handshake and lists the tools advertised by the server. It must confirm that `web_search` and `web_fetch` are available.

The probe deliberately does **not** invoke either tool and does not make a Gemini call. It is excluded from CI and from the standard local readiness script because those checks must remain fully offline and reproducible.

Run it manually from the active virtual environment with:

```powershell
python scripts/check_parallel_mcp.py
```

A successful result ends with:

```text
PARALLEL_MCP_CONNECTIVITY=PASS
TOOL_INVOCATIONS=0
GEMINI_CALLS=0
```

## Deferred work

The credentialled Gemini → Parallel runtime acceptance test remains deferred until a dedicated Google Cloud project can use the hackathon credits. No production project should be repurposed merely to complete that test.
