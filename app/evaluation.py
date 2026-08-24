"""Deterministic, at-no-cost evaluation utilities for CineScout AI."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.contracts import REQUIRED_RESPONSE_SECTIONS, ResearchCategory


@dataclass(frozen=True)
class EvaluationScenario:
    """One controlled production-research scenario."""

    scenario_id: str
    title: str
    brief: str
    expected_research_categories: tuple[ResearchCategory, ...]
    required_response_sections: tuple[str, ...]


def _as_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _parse_scenario(raw: Any) -> EvaluationScenario:
    if not isinstance(raw, dict):
        raise ValueError("each evaluation scenario must be a JSON object")

    categories_raw = raw.get("expected_research_categories")
    if not isinstance(categories_raw, list) or not categories_raw:
        raise ValueError("expected_research_categories must be a non-empty list")

    try:
        categories = tuple(ResearchCategory(item) for item in categories_raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("evaluation scenario contains an unknown research category") from exc

    sections_raw = raw.get("required_response_sections")
    if not isinstance(sections_raw, list):
        raise ValueError("required_response_sections must be a list")
    sections = tuple(_as_non_empty_string(item, "required_response_sections item") for item in sections_raw)

    if sections != REQUIRED_RESPONSE_SECTIONS:
        raise ValueError("required_response_sections must match the Phase 1 response contract")

    return EvaluationScenario(
        scenario_id=_as_non_empty_string(raw.get("id"), "id"),
        title=_as_non_empty_string(raw.get("title"), "title"),
        brief=_as_non_empty_string(raw.get("brief"), "brief"),
        expected_research_categories=categories,
        required_response_sections=sections,
    )


def load_scenarios(path: str | Path) -> tuple[EvaluationScenario, ...]:
    """Load and validate the controlled evaluation corpus."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError("evaluation corpus must be a non-empty JSON list")

    scenarios = tuple(_parse_scenario(item) for item in payload)
    identifiers = [scenario.scenario_id for scenario in scenarios]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("evaluation scenario IDs must be unique")
    return scenarios


def missing_response_sections(response_text: str) -> tuple[str, ...]:
    """Return required response headings that are absent from an agent response."""

    normalised = response_text.casefold()
    return tuple(section for section in REQUIRED_RESPONSE_SECTIONS if section.casefold() not in normalised)
