"""Tests for the deterministic CineScout evaluation contract."""

from app.contracts import REQUIRED_RESPONSE_SECTIONS, EvidenceStatus, ResearchCategory
from app.evaluation import load_scenarios, missing_response_sections


def test_controlled_evaluation_corpus_is_valid() -> None:
    scenarios = load_scenarios("evals/scenarios.json")

    assert len(scenarios) >= 6
    assert len({scenario.scenario_id for scenario in scenarios}) == len(scenarios)
    assert all(
        scenario.required_response_sections == REQUIRED_RESPONSE_SECTIONS
        for scenario in scenarios
    )
    assert all(scenario.expected_research_categories for scenario in scenarios)


def test_evaluation_corpus_covers_core_research_categories() -> None:
    scenarios = load_scenarios("evals/scenarios.json")
    covered = {
        category
        for scenario in scenarios
        for category in scenario.expected_research_categories
    }

    assert ResearchCategory.HISTORICAL_CONTEXT in covered
    assert ResearchCategory.CULTURAL_CONTEXT in covered
    assert ResearchCategory.GEOGRAPHY_LOCATION in covered
    assert ResearchCategory.INSTITUTION in covered
    assert ResearchCategory.PROP_OR_TECHNOLOGY in covered
    assert ResearchCategory.TERMINOLOGY in covered
    assert ResearchCategory.LOGISTICS in covered
    assert ResearchCategory.RIGHTS_CONTEXT in covered


def test_missing_response_sections_reports_only_absent_headings() -> None:
    response = "\n".join(
        (
            "Production reading",
            "Evidence and verification",
            "Production implications",
            "Sources consulted",
        )
    )

    assert missing_response_sections(response) == ("Uncertainty or conflicts",)


def test_evidence_status_supports_insufficient_evidence() -> None:
    assert EvidenceStatus.INSUFFICIENT_EVIDENCE.value == "insufficient_evidence"
