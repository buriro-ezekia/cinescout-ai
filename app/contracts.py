"""Shared domain contracts for CineScout AI production research."""

from __future__ import annotations

from enum import StrEnum


class ResearchCategory(StrEnum):
    """Externally verifiable production-research categories."""

    HISTORICAL_CONTEXT = "historical_context"
    CULTURAL_CONTEXT = "cultural_context"
    GEOGRAPHY_LOCATION = "geography_location"
    INSTITUTION = "institution"
    PROP_OR_TECHNOLOGY = "prop_or_technology"
    TERMINOLOGY = "terminology"
    LOGISTICS = "logistics"
    RIGHTS_CONTEXT = "rights_context"


class EvidenceStatus(StrEnum):
    """Evidence confidence labels available to later orchestration stages."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


REQUIRED_RESPONSE_SECTIONS: tuple[str, ...] = (
    "Production reading",
    "Evidence and verification",
    "Production implications",
    "Uncertainty or conflicts",
    "Sources consulted",
)
