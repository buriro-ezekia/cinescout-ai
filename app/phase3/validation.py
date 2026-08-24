"""Deterministic validators for CineScout AI Phase 3 resilience fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.contracts import REQUIRED_RESPONSE_SECTIONS, EvidenceStatus
from app.phase2.contracts import (
    MAX_RESEARCH_TASKS,
    MAX_WEB_FETCH_CALLS,
    MAX_WEB_SEARCH_CALLS,
)
from app.phase3.contracts import (
    EVIDENCE_STATUS_RANK,
    REQUIRED_RESILIENCE_PROPERTIES,
    ResilienceIssue,
    ResilienceIssueCode,
    ResilienceResult,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESILIENCE_PATH = REPO_ROOT / "evals" / "resilience_scenarios.json"


def load_resilience_scenarios(path: Path | None = None) -> tuple[dict[str, Any], ...]:
    """Load controlled Phase 3 resilience scenarios from JSON."""

    source = path or DEFAULT_RESILIENCE_PATH
    payload = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Resilience corpus must be a JSON list.")
    return tuple(payload)


def _status(value: str) -> EvidenceStatus:
    return EvidenceStatus(value)


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _has_duplicates(values: list[str]) -> bool:
    return len(values) != len(set(values))


def _valid_shape(scenario: dict[str, Any]) -> bool:
    required_top = {
        "id",
        "description",
        "properties",
        "expected_valid",
        "expected_issue_codes",
        "brief_analysis",
        "research_plan",
        "evidence_review",
        "risk_assessment",
        "final_report",
    }
    if not required_top.issubset(scenario):
        return False
    if not isinstance(scenario["id"], str) or not scenario["id"]:
        return False
    if not isinstance(scenario["description"], str):
        return False
    if not _is_string_list(scenario["properties"]):
        return False
    if not isinstance(scenario["expected_valid"], bool):
        return False
    if not _is_string_list(scenario["expected_issue_codes"]):
        return False

    brief = scenario["brief_analysis"]
    plan = scenario["research_plan"]
    evidence = scenario["evidence_review"]
    risk = scenario["risk_assessment"]
    report = scenario["final_report"]
    stages = (brief, plan, evidence, risk, report)
    if not all(isinstance(stage, dict) for stage in stages):
        return False
    if not isinstance(brief.get("claims"), list):
        return False
    if not isinstance(plan.get("tasks"), list):
        return False
    if not isinstance(evidence.get("claims"), list):
        return False
    if not isinstance(evidence.get("usage"), dict):
        return False
    if not isinstance(risk.get("claims"), list):
        return False
    if not _is_string_list(report.get("retained_claim_ids")):
        return False
    if not isinstance(report.get("claim_statuses"), dict):
        return False
    if not _is_string_list(report.get("source_ids")):
        return False
    if not _is_string_list(report.get("unresolved_claim_ids")):
        return False
    if not _is_string_list(report.get("sections")):
        return False

    for claim in brief["claims"]:
        if not isinstance(claim, dict):
            return False
        if not isinstance(claim.get("claim_id"), str):
            return False
        if not isinstance(claim.get("requires_research"), bool):
            return False

    for task in plan["tasks"]:
        if not isinstance(task, dict):
            return False
        if not isinstance(task.get("task_id"), str):
            return False
        if not isinstance(task.get("claim_id"), str):
            return False

    for claim in evidence["claims"]:
        if not isinstance(claim, dict):
            return False
        if not isinstance(claim.get("claim_id"), str):
            return False
        if not _is_string_list(claim.get("sources")):
            return False
        if not isinstance(claim.get("conflict"), bool):
            return False
        if not isinstance(claim.get("uncertainty"), str):
            return False
        try:
            _status(claim.get("status", ""))
        except (TypeError, ValueError):
            return False

    usage = evidence["usage"]
    for key in ("web_search_calls", "web_fetch_calls"):
        value = usage.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            return False

    for claim in risk["claims"]:
        if not isinstance(claim, dict):
            return False
        if not isinstance(claim.get("claim_id"), str):
            return False
        if not isinstance(claim.get("uncertainty"), str):
            return False
        try:
            _status(claim.get("status", ""))
        except (TypeError, ValueError):
            return False

    claim_statuses = report["claim_statuses"]
    if not all(isinstance(key, str) for key in claim_statuses):
        return False
    try:
        for value in claim_statuses.values():
            _status(value)
    except (TypeError, ValueError):
        return False
    return True


def validate_resilience_scenario(scenario: dict[str, Any]) -> ResilienceResult:
    """Validate one controlled stage-state scenario against Phase 3 invariants."""

    raw_id = scenario.get("id", "<malformed>")
    scenario_id = raw_id if isinstance(raw_id, str) else "<malformed>"
    issues: dict[ResilienceIssueCode, ResilienceIssue] = {}

    def add(code: ResilienceIssueCode, message: str) -> None:
        issues.setdefault(code, ResilienceIssue(code=code, message=message))

    if not _valid_shape(scenario):
        add(ResilienceIssueCode.MALFORMED_STATE, "Scenario stage state is malformed.")
        return ResilienceResult(scenario_id=scenario_id, issues=tuple(issues.values()))

    brief_claims = scenario["brief_analysis"]["claims"]
    tasks = scenario["research_plan"]["tasks"]
    evidence_claims = scenario["evidence_review"]["claims"]
    usage = scenario["evidence_review"]["usage"]
    risk_claims = scenario["risk_assessment"]["claims"]
    report = scenario["final_report"]

    claim_ids = [claim["claim_id"] for claim in brief_claims]
    task_ids = [task["task_id"] for task in tasks]
    evidence_ids = [claim["claim_id"] for claim in evidence_claims]
    risk_ids = [claim["claim_id"] for claim in risk_claims]
    final_source_ids = report["source_ids"]
    retained_ids = report["retained_claim_ids"]
    unresolved_ids = report["unresolved_claim_ids"]

    identifier_groups = (
        claim_ids,
        task_ids,
        evidence_ids,
        risk_ids,
        retained_ids,
        unresolved_ids,
    )
    if any(_has_duplicates(values) for values in identifier_groups):
        add(ResilienceIssueCode.DUPLICATE_IDENTIFIER, "Stage identifiers must be unique.")
    if _has_duplicates(final_source_ids):
        add(ResilienceIssueCode.DUPLICATE_IDENTIFIER, "Final source identifiers must be unique.")

    known_claims = set(claim_ids)
    research_claims = {
        claim["claim_id"] for claim in brief_claims if claim["requires_research"]
    }
    task_claims = {task["claim_id"] for task in tasks}
    if any(task["claim_id"] not in known_claims for task in tasks):
        add(ResilienceIssueCode.UNKNOWN_TASK_CLAIM, "A research task references an unknown claim.")
    if research_claims and not task_claims:
        add(
            ResilienceIssueCode.EMPTY_PLAN_WITH_RESEARCH,
            "Externally verifiable claims require a non-empty research plan.",
        )
    elif research_claims - task_claims:
        add(
            ResilienceIssueCode.MISSING_RESEARCH_TASK,
            "Every externally verifiable claim must receive a research task.",
        )

    if len(tasks) > MAX_RESEARCH_TASKS:
        add(ResilienceIssueCode.RESEARCH_BUDGET_EXCEEDED, "Research-task budget exceeded.")
    search_calls = usage["web_search_calls"]
    fetch_calls = usage["web_fetch_calls"]
    if search_calls > MAX_WEB_SEARCH_CALLS:
        add(ResilienceIssueCode.SEARCH_BUDGET_EXCEEDED, "web_search budget exceeded.")
    if fetch_calls > MAX_WEB_FETCH_CALLS:
        add(ResilienceIssueCode.FETCH_BUDGET_EXCEEDED, "web_fetch budget exceeded.")
    if search_calls > len(tasks):
        add(
            ResilienceIssueCode.SEARCH_PER_TASK_EXCEEDED,
            "At most one web_search call is permitted per planned task.",
        )

    evidence_by_id = {claim["claim_id"]: claim for claim in evidence_claims}
    risk_by_id = {claim["claim_id"]: claim for claim in risk_claims}
    missing_evidence = research_claims - set(evidence_by_id)
    if missing_evidence:
        add(
            ResilienceIssueCode.MISSING_EVIDENCE,
            "Every externally verifiable claim must reach evidence review.",
        )
    missing_risk = set(evidence_by_id) - set(risk_by_id)
    if missing_risk:
        add(
            ResilienceIssueCode.MISSING_RISK_ASSESSMENT,
            "Every evidence-reviewed claim must reach production-risk assessment.",
        )

    unresolved_claims: set[str] = set()
    for claim_id, evidence in evidence_by_id.items():
        status = _status(evidence["status"])
        sources = evidence["sources"]
        conflict = evidence["conflict"]
        uncertainty = evidence["uncertainty"].strip()

        if not sources and status is not EvidenceStatus.INSUFFICIENT_EVIDENCE:
            add(
                ResilienceIssueCode.UNSUPPORTED_PROMOTED,
                f"Unsupported claim {claim_id} was promoted above insufficient evidence.",
            )
        if conflict and status is EvidenceStatus.HIGH:
            add(
                ResilienceIssueCode.CONFLICT_PROMOTED_HIGH,
                f"Conflicting claim {claim_id} cannot have high confidence.",
            )
        if conflict or status is EvidenceStatus.INSUFFICIENT_EVIDENCE or uncertainty:
            unresolved_claims.add(claim_id)

        downstream = risk_by_id.get(claim_id)
        if downstream is not None:
            risk_status = _status(downstream["status"])
            if EVIDENCE_STATUS_RANK[risk_status] > EVIDENCE_STATUS_RANK[status]:
                add(
                    ResilienceIssueCode.CONFIDENCE_ESCALATION,
                    f"Risk assessment increased confidence for {claim_id}.",
                )
            if claim_id in unresolved_claims and not downstream["uncertainty"].strip():
                add(
                    ResilienceIssueCode.UNCERTAINTY_DROPPED,
                    f"Risk assessment dropped uncertainty for {claim_id}.",
                )

    retained_claim_ids = set(retained_ids)
    final_statuses = report["claim_statuses"]
    final_unresolved = set(unresolved_ids)
    final_sources = set(final_source_ids)

    for claim_id in retained_claim_ids:
        evidence = evidence_by_id.get(claim_id)
        final_status_value = final_statuses.get(claim_id)
        if evidence is None or final_status_value is None:
            add(
                ResilienceIssueCode.FINAL_REPORT_CONTRACT_BROKEN,
                f"Retained claim {claim_id} lacks evidence or final confidence status.",
            )
            continue

        evidence_status = _status(evidence["status"])
        final_status = _status(final_status_value)
        if EVIDENCE_STATUS_RANK[final_status] > EVIDENCE_STATUS_RANK[evidence_status]:
            add(
                ResilienceIssueCode.CONFIDENCE_ESCALATION,
                f"Final report increased confidence for {claim_id}.",
            )
        if not set(evidence["sources"]).issubset(final_sources):
            add(
                ResilienceIssueCode.SOURCE_ATTRIBUTION_DROPPED,
                f"Final report dropped source attribution for {claim_id}.",
            )
        if claim_id in unresolved_claims and claim_id not in final_unresolved:
            add(
                ResilienceIssueCode.UNCERTAINTY_DROPPED,
                f"Final report dropped unresolved status for {claim_id}.",
            )

    if tuple(report["sections"]) != REQUIRED_RESPONSE_SECTIONS:
        add(
            ResilienceIssueCode.FINAL_REPORT_CONTRACT_BROKEN,
            "Final report sections do not match the required ordered contract.",
        )

    return ResilienceResult(scenario_id=scenario_id, issues=tuple(issues.values()))


def validate_resilience_corpus(
    scenarios: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    """Validate corpus expectations, coverage and uniqueness."""

    failures: list[str] = []
    scenario_ids = [scenario.get("id") for scenario in scenarios]
    if len(scenario_ids) != len(set(scenario_ids)):
        failures.append("Scenario IDs must be unique.")

    covered_properties = {
        property_name
        for scenario in scenarios
        if isinstance(scenario.get("properties"), list)
        for property_name in scenario["properties"]
        if isinstance(property_name, str)
    }
    missing_properties = REQUIRED_RESILIENCE_PROPERTIES - covered_properties
    if missing_properties:
        failures.append(
            "Missing resilience property coverage: " + ",".join(sorted(missing_properties))
        )

    for scenario in scenarios:
        result = validate_resilience_scenario(scenario)
        expected_valid = scenario.get("expected_valid")
        expected_codes = set(scenario.get("expected_issue_codes", []))
        actual_codes = {issue.code.value for issue in result.issues}
        if result.is_valid is not expected_valid:
            failures.append(
                f"{result.scenario_id}: expected_valid={expected_valid}, actual={result.is_valid}"
            )
        if actual_codes != expected_codes:
            failures.append(
                f"{result.scenario_id}: expected={sorted(expected_codes)}, "
                f"actual={sorted(actual_codes)}"
            )
    return tuple(failures)
