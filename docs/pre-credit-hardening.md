# Pre-credit hardening

CineScout AI can continue to make meaningful engineering progress before Google Cloud hackathon credits are available. This work deliberately excludes Gemini and Vertex AI requests so that routine development remains at no cost.

## Purpose

The pre-credit hardening layer prepares the repository for the eventual credentialled Gemini → Parallel acceptance tests without weakening the project's evidence requirements or introducing a substitute model. It concentrates on deterministic contracts, controlled evaluation scenarios, dependency integrity, specialist-workflow structure and partner-connectivity checks.

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
Phase 1 repository contract
    |
    v
Phase 2 graph-workflow contract
```

The controlled corpus in `evals/scenarios.json` covers historical context, cultural context, geography and locations, institutions, props or technology, terminology, logistics and rights context. These scenarios do not attempt to answer the research questions offline. Instead, they define what later live evaluations must recognise and how the final response must be structured.

## Production-research contract

`app/contracts.py` defines the shared research categories, evidence-status vocabulary and required response sections. These contracts are consumed by the Phase 2 specialist workflow so all stages use the same evidence language and final-response structure.

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

## Phase 2 offline workflow boundary

Phase 2 is implemented as a graph-based Google ADK `Workflow` with five specialist LLM nodes. Structural validation may construct the workflow and inspect its graph, state keys, tool ownership and specialist configuration, but it must not execute an agent.

Only the Evidence Verifier owns Parallel Search MCP. All specialists are isolated `single_turn` workflow nodes with `include_contents="none"`. The offline contract therefore validates architecture without consuming Gemini or Parallel search capacity.

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

The credentialled Gemini → Parallel runtime acceptance tests remain deferred until a dedicated Google Cloud project can use the hackathon credits. No unrelated production project should be repurposed merely to complete those tests.
