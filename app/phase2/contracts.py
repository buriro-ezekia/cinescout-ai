"""Structural contracts for the CineScout AI Phase 2 pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SpecialistRole(StrEnum):
    """Specialist roles executed by the Phase 2 workflow."""

    BRIEF_INTERPRETER = "brief_interpreter"
    RESEARCH_PLANNER = "research_planner"
    EVIDENCE_VERIFIER = "evidence_verifier"
    PRODUCTION_RISK = "production_risk"
    REPORT_SYNTHESISER = "report_synthesiser"


@dataclass(frozen=True)
class StageContract:
    """One deterministic specialist stage and its shared-state output."""

    role: SpecialistRole
    agent_name: str
    output_key: str
    uses_parallel: bool = False


MAX_RESEARCH_TASKS = 6
MAX_WEB_SEARCH_CALLS = 6
MAX_WEB_FETCH_CALLS = 3

PHASE2_STAGES: tuple[StageContract, ...] = (
    StageContract(
        role=SpecialistRole.BRIEF_INTERPRETER,
        agent_name="cinescout_brief_interpreter",
        output_key="phase2_brief_analysis",
    ),
    StageContract(
        role=SpecialistRole.RESEARCH_PLANNER,
        agent_name="cinescout_research_planner",
        output_key="phase2_research_plan",
    ),
    StageContract(
        role=SpecialistRole.EVIDENCE_VERIFIER,
        agent_name="cinescout_evidence_verifier",
        output_key="phase2_evidence_review",
        uses_parallel=True,
    ),
    StageContract(
        role=SpecialistRole.PRODUCTION_RISK,
        agent_name="cinescout_production_risk",
        output_key="phase2_risk_assessment",
    ),
    StageContract(
        role=SpecialistRole.REPORT_SYNTHESISER,
        agent_name="cinescout_report_synthesiser",
        output_key="phase2_final_report",
    ),
)

PHASE2_STAGE_ORDER: tuple[SpecialistRole, ...] = tuple(
    stage.role for stage in PHASE2_STAGES
)


def stage_contract(role: SpecialistRole) -> StageContract:
    """Return the contract for one specialist role."""

    return next(stage for stage in PHASE2_STAGES if stage.role is role)
