# Phase 2 — Specialist agent architecture specification

## Objective

Phase 2 extends the validated CineScout AI Phase 1 vertical slice into a deterministic specialist-agent workflow without replacing the proven Phase 1 entry point. The design separates interpretation, research planning, evidence verification, production-risk assessment and report synthesis so that each stage has one clear responsibility and an auditable state hand-off.

The Phase 2 implementation must remain testable at no cost while Google hackathon credits are pending. Import checks, structural checks, evaluation contracts and repository readiness must therefore make zero Gemini calls and zero external search calls.

## Specialist workflow

The Phase 2 candidate is:

```text
Production brief or screenplay extract
        |
        v
Brief Interpreter
        |
        | phase2_brief_analysis
        v
Research Planner
        |
        | phase2_research_plan
        v
Evidence Verifier  ----> Parallel Search MCP
        |
        | phase2_evidence_review
        v
Production Risk Agent
        |
        | phase2_risk_assessment
        v
Report Synthesiser
        |
        | phase2_final_report
        v
Evidence-backed production intelligence
```

Google ADK `Workflow` provides the orchestration layer. The graph is a strict chain from `START` through the five specialist LLM nodes, which preserves deterministic execution order without relying on the deprecated `SequentialAgent` convenience wrapper.

Every specialist is created through a factory function and is explicitly configured as a `single_turn` workflow node with `include_contents="none"`. Each specialist therefore receives the immediate workflow input and the state values referenced by its instruction without inheriting unrelated conversation history.

The module exports both descriptive names (`phase2_root_agent`, `phase2_app`) and the conventional ADK loader names (`root_agent`, `app`). This keeps Phase 2 separately runnable later without changing the repository's default Phase 1 entry point.

## Responsibilities

### Brief Interpreter

The Brief Interpreter reads the user's production brief and identifies externally verifiable claims, creative judgements, assumptions and missing context. It must classify research needs using the shared CineScout research categories. It does not perform external research.

### Research Planner

The Research Planner converts the brief analysis into a bounded research plan. It prioritises material claims, defines concise research questions and identifies the evidence needed to support a production decision. It does not perform external research.

The plan must remain deliberately bounded for the hackathon prototype: no more than six research tasks should be proposed for a single run unless the user explicitly requests broader research.

### Evidence Verifier

The Evidence Verifier is the only Phase 2 specialist with direct access to Parallel Search MCP. It executes the research plan, uses `web_search` for externally verifiable claims and uses `web_fetch` only when a particular source requires closer inspection.

For the default bounded workflow, it should make no more than one `web_search` call per planned research task and no more than three `web_fetch` calls in total unless the user explicitly requests deeper research. It must distinguish supported evidence, conflicting evidence and insufficient evidence. It must never invent sources or label an unsupported claim as verified.

### Production Risk Agent

The Production Risk Agent converts the verified evidence into production implications. It identifies continuity, authenticity, cultural, logistical, rights-context and other production risks without presenting its output as legal clearance, professional safety advice or an authoritative cultural ruling.

### Report Synthesiser

The Report Synthesiser produces the final user-facing production intelligence response. It must use the established five-section response contract:

- Production reading
- Evidence and verification
- Production implications
- Uncertainty or conflicts
- Sources consulted

It must preserve uncertainty and must not strengthen the certainty of upstream evidence.

## Shared state contract

The workflow must use these output keys exactly:

- `phase2_brief_analysis`
- `phase2_research_plan`
- `phase2_evidence_review`
- `phase2_risk_assessment`
- `phase2_final_report`

ADK workflow nodes pass their output to the next node and each specialist also writes its final output into session state through `output_key`. Later specialists may therefore consume prior outputs through explicit state placeholders without hidden module coupling.

## Partner integration boundary

Parallel Search MCP remains the external research layer. Only the Evidence Verifier receives the MCP toolset. This makes partner usage observable and prevents unrelated specialists from performing unnecessary searches.

The existing Phase 1 Parallel configuration remains unchanged. Phase 2 creates its own MCP toolset instance through a factory so the Phase 1 root agent is not modified.

## Cost and execution boundary

Before Google hackathon credits are available:

- the Phase 1 root agent remains the repository default;
- the Phase 2 workflow may be imported and structurally validated;
- no Phase 2 test may invoke Gemini;
- no Phase 2 automated test may invoke Parallel `web_search` or `web_fetch`;
- the existing manual Parallel connectivity probe may continue to list tools without invoking them.

The Phase 2 candidate becomes eligible for a credentialled live acceptance test only after a dedicated CineScout AI Google Cloud project has the intended hackathon credit arrangement.

## Acceptance criteria

Phase 2 offline implementation is complete when all of the following are true:

1. A five-stage ADK `Workflow` exists as one strict graph chain in the exact specialist order defined above.
2. Every specialist has a distinct output key matching the shared state contract.
3. Every specialist is an isolated `single_turn` node with `include_contents="none"`.
4. Specialist factory functions create fresh agent instances for repeated workflow construction.
5. Only the Evidence Verifier has a Parallel MCP toolset.
6. The Evidence Verifier is explicitly instructed to research externally verifiable claims and preserve evidence uncertainty.
7. The Report Synthesiser is explicitly constrained to the existing five-section response contract.
8. The Phase 1 `app/agent.py` entry point remains unchanged by Phase 2 implementation.
9. The Phase 2 module exports conventional ADK `root_agent` and `app` names without replacing Phase 1 defaults.
10. Local readiness includes a Phase 2 structural contract check that makes zero Gemini calls and zero external search calls.
11. Automated tests verify graph order, state keys, tool ownership, specialist isolation, factory isolation, ADK exports and the at-no-cost execution boundary.
12. README and Phase 2 documentation describe the architecture accurately in professional UK English.
13. Phase 2 production code contains no dependency on deprecated `SequentialAgent` orchestration.

## Deferred live acceptance

The later credentialled acceptance test must demonstrate one complete run in which Gemini executes the five-stage workflow, the Evidence Verifier invokes Parallel Search MCP at runtime, evidence reaches the downstream risk and synthesis stages, and the final response preserves sources and uncertainty.
