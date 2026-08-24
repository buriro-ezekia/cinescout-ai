"""Google ADK candidate workflow for CineScout AI Phase 2."""

from __future__ import annotations

from google.adk import START, Workflow
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.config import settings
from app.phase2.contracts import SpecialistRole, stage_contract
from app.phase2.prompts import (
    BRIEF_INTERPRETER_INSTRUCTION,
    EVIDENCE_VERIFIER_INSTRUCTION,
    PRODUCTION_RISK_INSTRUCTION,
    REPORT_SYNTHESISER_INSTRUCTION,
    RESEARCH_PLANNER_INSTRUCTION,
)
from app.phase2.tools import create_parallel_search_toolset


def _model() -> Gemini:
    """Create a fresh Gemini model configuration without invoking the model."""

    return Gemini(
        model=settings.model,
        retry_options=types.HttpRetryOptions(attempts=3),
    )


def _specialist_agent(
    *,
    role: SpecialistRole,
    description: str,
    instruction: str,
    tools: list | None = None,
) -> Agent:
    """Create one isolated single-turn specialist workflow node."""

    contract = stage_contract(role)
    return Agent(
        name=contract.agent_name,
        model=_model(),
        mode="single_turn",
        include_contents="none",
        description=description,
        instruction=instruction,
        tools=tools or [],
        output_key=contract.output_key,
    )


def create_brief_interpreter() -> Agent:
    """Create the specialist that interprets the production brief."""

    return _specialist_agent(
        role=SpecialistRole.BRIEF_INTERPRETER,
        description="Identifies production claims and context that require verification.",
        instruction=BRIEF_INTERPRETER_INSTRUCTION,
    )


def create_research_planner() -> Agent:
    """Create the specialist that converts brief analysis into bounded research tasks."""

    return _specialist_agent(
        role=SpecialistRole.RESEARCH_PLANNER,
        description="Builds a bounded external-research plan from the interpreted brief.",
        instruction=RESEARCH_PLANNER_INSTRUCTION,
    )


def create_evidence_verifier() -> Agent:
    """Create the only specialist with direct access to Parallel Search MCP."""

    return _specialist_agent(
        role=SpecialistRole.EVIDENCE_VERIFIER,
        description="Executes the research plan and assesses source-backed evidence.",
        instruction=EVIDENCE_VERIFIER_INSTRUCTION,
        tools=[create_parallel_search_toolset()],
    )


def create_production_risk_agent() -> Agent:
    """Create the specialist that converts evidence into production implications."""

    return _specialist_agent(
        role=SpecialistRole.PRODUCTION_RISK,
        description="Assesses practical production risks without overstating evidence.",
        instruction=PRODUCTION_RISK_INSTRUCTION,
    )


def create_report_synthesiser() -> Agent:
    """Create the specialist that produces the final production intelligence report."""

    return _specialist_agent(
        role=SpecialistRole.REPORT_SYNTHESISER,
        description="Synthesises evidence, risk and uncertainty into the final response.",
        instruction=REPORT_SYNTHESISER_INSTRUCTION,
    )


def create_phase2_specialists() -> tuple[Agent, ...]:
    """Create fresh specialist nodes in the canonical Phase 2 order."""

    return (
        create_brief_interpreter(),
        create_research_planner(),
        create_evidence_verifier(),
        create_production_risk_agent(),
        create_report_synthesiser(),
    )


def create_phase2_pipeline() -> Workflow:
    """Create a fresh deterministic five-stage graph workflow."""

    specialists = create_phase2_specialists()
    return Workflow(
        name="cinescout_phase2_pipeline",
        description=(
            "Deterministic specialist workflow for evidence-backed pre-production research."
        ),
        edges=[(START, *specialists)],
    )


phase2_root_agent = create_phase2_pipeline()
phase2_app = App(
    root_agent=phase2_root_agent,
    name="phase2_app",
)
