"""Google ADK candidate pipeline for CineScout AI Phase 2."""

from __future__ import annotations

from google.adk.agents import Agent, SequentialAgent
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


def create_brief_interpreter() -> Agent:
    """Create the specialist that interprets the production brief."""

    contract = stage_contract(SpecialistRole.BRIEF_INTERPRETER)
    return Agent(
        name=contract.agent_name,
        model=_model(),
        description="Identifies production claims and context that require verification.",
        instruction=BRIEF_INTERPRETER_INSTRUCTION,
        output_key=contract.output_key,
    )


def create_research_planner() -> Agent:
    """Create the specialist that converts brief analysis into bounded research tasks."""

    contract = stage_contract(SpecialistRole.RESEARCH_PLANNER)
    return Agent(
        name=contract.agent_name,
        model=_model(),
        description="Builds a bounded external-research plan from the interpreted brief.",
        instruction=RESEARCH_PLANNER_INSTRUCTION,
        output_key=contract.output_key,
    )


def create_evidence_verifier() -> Agent:
    """Create the only specialist with direct access to Parallel Search MCP."""

    contract = stage_contract(SpecialistRole.EVIDENCE_VERIFIER)
    return Agent(
        name=contract.agent_name,
        model=_model(),
        description="Executes the research plan and assesses source-backed evidence.",
        instruction=EVIDENCE_VERIFIER_INSTRUCTION,
        tools=[create_parallel_search_toolset()],
        output_key=contract.output_key,
    )


def create_production_risk_agent() -> Agent:
    """Create the specialist that converts evidence into production implications."""

    contract = stage_contract(SpecialistRole.PRODUCTION_RISK)
    return Agent(
        name=contract.agent_name,
        model=_model(),
        description="Assesses practical production risks without overstating evidence.",
        instruction=PRODUCTION_RISK_INSTRUCTION,
        output_key=contract.output_key,
    )


def create_report_synthesiser() -> Agent:
    """Create the specialist that produces the final production intelligence report."""

    contract = stage_contract(SpecialistRole.REPORT_SYNTHESISER)
    return Agent(
        name=contract.agent_name,
        model=_model(),
        description="Synthesises evidence, risk and uncertainty into the final response.",
        instruction=REPORT_SYNTHESISER_INSTRUCTION,
        output_key=contract.output_key,
    )


def create_phase2_pipeline() -> SequentialAgent:
    """Create a fresh deterministic five-stage Phase 2 pipeline."""

    return SequentialAgent(
        name="cinescout_phase2_pipeline",
        description=(
            "Deterministic specialist workflow for evidence-backed pre-production research."
        ),
        sub_agents=[
            create_brief_interpreter(),
            create_research_planner(),
            create_evidence_verifier(),
            create_production_risk_agent(),
            create_report_synthesiser(),
        ],
    )


phase2_root_agent = create_phase2_pipeline()
phase2_app = App(
    root_agent=phase2_root_agent,
    name="phase2_app",
)
