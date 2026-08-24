"""Contracts for deterministic CineScout AI Phase 3 resilience evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.contracts import EvidenceStatus


class ResilienceIssueCode(StrEnum):
    """Stable machine-readable failure codes for resilience validation."""

    MALFORMED_STATE = "malformed_state"
    EMPTY_PLAN_WITH_RESEARCH = "empty_plan_with_research"
    UNKNOWN_TASK_CLAIM = "unknown_task_claim"
    DUPLICATE_IDENTIFIER = "duplicate_identifier"
    MISSING_EVIDENCE = "missing_evidence"
    UNSUPPORTED_PROMOTED = "unsupported_promoted"
    CONFLICT_PROMOTED_HIGH = "conflict_promoted_high"
    CONFIDENCE_ESCALATION = "confidence_escalation"
    SOURCE_ATTRIBUTION_DROPPED = "source_attribution_dropped"
    UNCERTAINTY_DROPPED = "uncertainty_dropped"
    RESEARCH_BUDGET_EXCEEDED = "research_budget_exceeded"
    SEARCH_BUDGET_EXCEEDED = "search_budget_exceeded"
    FETCH_BUDGET_EXCEEDED = "fetch_budget_exceeded"
    SEARCH_PER_TASK_EXCEEDED = "search_per_task_exceeded"
    FINAL_REPORT_CONTRACT_BROKEN = "final_report_contract_broken"


@dataclass(frozen=True)
class ResilienceIssue:
    """One deterministic validation failure."""

    code: ResilienceIssueCode
    message: str


@dataclass(frozen=True)
class ResilienceResult:
    """Validation result for one controlled resilience scenario."""

    scenario_id: str
    issues: tuple[ResilienceIssue, ...]

    @property
    def is_valid(self) -> bool:
        """Return whether the scenario satisfies every resilience invariant."""

        return not self.issues


EVIDENCE_STATUS_RANK: dict[EvidenceStatus, int] = {
    EvidenceStatus.INSUFFICIENT_EVIDENCE: 0,
    EvidenceStatus.LOW: 1,
    EvidenceStatus.MEDIUM: 2,
    EvidenceStatus.HIGH: 3,
}


REQUIRED_RESILIENCE_PROPERTIES: frozenset[str] = frozenset(
    {
        "malformed_state_rejection",
        "empty_plan_handling",
        "unsupported_claim_handling",
        "conflicting_evidence_handling",
        "confidence_non_escalation",
        "source_preservation",
        "uncertainty_propagation",
        "budget_enforcement",
        "final_report_contract",
    }
)
