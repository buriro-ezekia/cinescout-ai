# Phase 3 — Deterministic workflow evaluation and resilience

## Objective

Phase 3 strengthens CineScout AI without changing the validated Phase 1 or Phase 2 runtime architecture. It adds deterministic evaluation of state transitions and failure modes so the repository can prove that uncertainty, source attribution, evidence confidence and research budgets are preserved when upstream outputs are incomplete, malformed or contradictory.

The Phase 3 layer must remain testable at no cost while Google hackathon credits are pending. It therefore makes zero Gemini calls and zero Parallel search invocations.

## Resilience properties

Phase 3 validates these properties:

1. malformed stage payloads are rejected rather than silently accepted;
2. an empty research plan is valid only when the brief contains no externally verifiable claim;
3. unsupported claims remain `insufficient_evidence`;
4. conflicting evidence cannot be promoted to `high` confidence;
5. downstream stages cannot increase evidence confidence;
6. source attribution survives downstream transformations;
7. unresolved uncertainty survives risk assessment and final synthesis;
8. research-task, `web_search` and `web_fetch` budgets remain bounded;
9. final reports retain the required five-section contract; and
10. all deterministic fixtures can be validated without executing the ADK workflow.

## Fixture model

The controlled resilience corpus lives in `evals/resilience_scenarios.json`. Each scenario contains explicit stage-state snapshots rather than model-generated text. This allows deterministic validation of the contract independently of Gemini or external web access.

Each fixture records:

- brief analysis;
- research plan;
- evidence review;
- production-risk assessment;
- final report;
- expected validation outcome; and
- the resilience properties exercised by the scenario.

## Evidence confidence order

CineScout recognises these evidence states:

```text
insufficient_evidence < low < medium < high
```

A downstream stage may preserve or reduce confidence but must never increase it beyond the Evidence Verifier's status for the same claim.

Conflicting evidence is never eligible for `high` confidence. Unsupported claims must remain `insufficient_evidence`.

## Source preservation

Every source identifier attached to a material claim in the Evidence Verifier output must remain attributable in the final report. A downstream stage may cite fewer sources only for claims omitted from the final response; it must not detach a retained claim from all of its supporting source identifiers.

## Empty research plans

An empty research plan is allowed only when the Brief Interpreter reports no material externally verifiable claims. If verifiable claims exist, the plan must contain at least one research task.

## Budget contract

The existing Phase 2 bounds remain authoritative:

- maximum research tasks: 6;
- maximum `web_search` calls: 6;
- maximum `web_fetch` calls: 3.

Phase 3 validates fixture metadata against those bounds but does not make live tool calls.

## Final report contract

Every valid final-report fixture must contain these sections exactly once and in this order:

1. Production reading
2. Evidence and verification
3. Production implications
4. Uncertainty or conflicts
5. Sources consulted

## Acceptance criteria

Phase 3 offline implementation is complete when:

- typed resilience contracts and validators exist;
- the controlled resilience corpus covers malformed input, empty plans, unsupported claims, conflicting evidence, confidence non-escalation, source preservation, uncertainty propagation, budget enforcement and final-report structure;
- unit tests exercise both passing and intentionally failing fixtures;
- a standalone Phase 3 readiness checker validates the corpus from outside the repository root;
- local readiness and CI invoke the Phase 3 checker after Phase 2;
- Phase 1 and Phase 2 runtime files remain unchanged by Phase 3; and
- all Phase 3 checks make zero Gemini calls and zero external search calls.

## Deferred live evaluation

After the intended Google hackathon credits are available, the deterministic Phase 3 fixtures become the basis for live evaluation. The live suite should compare real Gemini/Parallel runs against these invariants rather than replacing them.
