"""Deterministic tests for CineScout AI Phase 3 resilience evaluation."""

from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

from app.contracts import EvidenceStatus
from app.phase3.contracts import (
    EVIDENCE_STATUS_RANK,
    REQUIRED_RESILIENCE_PROPERTIES,
    ResilienceIssueCode,
)
from app.phase3.validation import (
    load_resilience_scenarios,
    validate_resilience_corpus,
    validate_resilience_scenario,
)


def test_phase3_corpus_matches_all_expected_outcomes() -> None:
    scenarios = load_resilience_scenarios()

    assert len(scenarios) == 15
    assert validate_resilience_corpus(scenarios) == ()
    assert sum(bool(scenario["expected_valid"]) for scenario in scenarios) == 4


def test_phase3_corpus_covers_every_required_resilience_property() -> None:
    scenarios = load_resilience_scenarios()
    covered = {
        property_name
        for scenario in scenarios
        for property_name in scenario["properties"]
    }

    assert REQUIRED_RESILIENCE_PROPERTIES <= covered


def test_evidence_status_order_is_monotonic() -> None:
    assert EVIDENCE_STATUS_RANK == {
        EvidenceStatus.INSUFFICIENT_EVIDENCE: 0,
        EvidenceStatus.LOW: 1,
        EvidenceStatus.MEDIUM: 2,
        EvidenceStatus.HIGH: 3,
    }


def test_valid_control_detects_downstream_confidence_escalation() -> None:
    scenario = copy.deepcopy(load_resilience_scenarios()[0])
    scenario["evidence_review"]["claims"][0]["status"] = "low"
    scenario["risk_assessment"]["claims"][0]["status"] = "medium"
    scenario["final_report"]["claim_statuses"]["c1"] = "medium"

    result = validate_resilience_scenario(scenario)

    assert not result.is_valid
    assert ResilienceIssueCode.CONFIDENCE_ESCALATION in {
        issue.code for issue in result.issues
    }


def test_valid_control_detects_source_loss() -> None:
    scenario = copy.deepcopy(load_resilience_scenarios()[0])
    scenario["final_report"]["source_ids"] = ["s1"]

    result = validate_resilience_scenario(scenario)

    assert not result.is_valid
    assert ResilienceIssueCode.SOURCE_ATTRIBUTION_DROPPED in {
        issue.code for issue in result.issues
    }


def test_partial_research_plan_is_rejected() -> None:
    scenario = copy.deepcopy(load_resilience_scenarios()[0])
    scenario["brief_analysis"]["claims"].append(
        {"claim_id": "c2", "requires_research": True}
    )
    scenario["evidence_review"]["claims"].append(
        {
            "claim_id": "c2",
            "status": "insufficient_evidence",
            "sources": [],
            "conflict": False,
            "uncertainty": "No research task was created.",
        }
    )
    scenario["risk_assessment"]["claims"].append(
        {
            "claim_id": "c2",
            "status": "insufficient_evidence",
            "uncertainty": "No research task was created.",
        }
    )

    result = validate_resilience_scenario(scenario)

    assert not result.is_valid
    assert {issue.code for issue in result.issues} == {
        ResilienceIssueCode.MISSING_RESEARCH_TASK
    }


def test_missing_production_risk_state_is_rejected() -> None:
    scenario = copy.deepcopy(load_resilience_scenarios()[0])
    scenario["risk_assessment"]["claims"] = []

    result = validate_resilience_scenario(scenario)

    assert not result.is_valid
    assert {issue.code for issue in result.issues} == {
        ResilienceIssueCode.MISSING_RISK_ASSESSMENT
    }


def test_malformed_stage_payload_fails_closed() -> None:
    scenario = copy.deepcopy(load_resilience_scenarios()[0])
    del scenario["evidence_review"]["usage"]

    result = validate_resilience_scenario(scenario)

    assert len(result.issues) == 1
    assert result.issues[0].code is ResilienceIssueCode.MALFORMED_STATE


def test_phase3_check_runs_outside_repository_root(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[2]
    script = repository_root / "scripts" / "check_phase3.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "PHASE3_RESILIENCE_SCENARIOS=15" in result.stdout
    assert "PHASE3_VALID_CONTROLS=4" in result.stdout
    assert "PHASE3_EXPECTED_FAILURE_CASES=11" in result.stdout
    assert "PHASE3_CONFIDENCE_NON_ESCALATION=PASS" in result.stdout
    assert "PHASE3_SOURCE_PRESERVATION=PASS" in result.stdout
    assert "PHASE3_UNCERTAINTY_PROPAGATION=PASS" in result.stdout
    assert "PHASE3_BUDGET_ENFORCEMENT=PASS" in result.stdout
    assert "PHASE3_GEMINI_CALLS=0" in result.stdout
    assert "PHASE3_EXTERNAL_SEARCH_CALLS=0" in result.stdout
    assert "PHASE3_RESILIENCE_CONTRACT=PASS" in result.stdout
