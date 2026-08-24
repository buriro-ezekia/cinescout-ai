"""Import-level integration tests for the Phase 2 ADK candidate."""

import pytest

pytest.importorskip("google.adk")

from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from app.phase2.agent import create_phase2_pipeline, phase2_app, phase2_root_agent
from app.phase2.contracts import PHASE2_STAGES, SpecialistRole


def test_phase2_application_imports_without_live_calls() -> None:
    assert isinstance(phase2_root_agent, SequentialAgent)
    assert phase2_root_agent.name == "cinescout_phase2_pipeline"
    assert phase2_app.name == "phase2_app"


def test_phase2_pipeline_matches_specialist_contract() -> None:
    pipeline = create_phase2_pipeline()
    agents = tuple(pipeline.sub_agents)

    assert len(agents) == 5
    assert tuple(agent.name for agent in agents) == tuple(
        stage.agent_name for stage in PHASE2_STAGES
    )
    assert tuple(agent.output_key for agent in agents) == tuple(
        stage.output_key for stage in PHASE2_STAGES
    )


def test_only_evidence_verifier_has_parallel_toolset() -> None:
    pipeline = create_phase2_pipeline()
    agents = tuple(pipeline.sub_agents)
    evidence_index = next(
        index
        for index, stage in enumerate(PHASE2_STAGES)
        if stage.role is SpecialistRole.EVIDENCE_VERIFIER
    )

    for index, agent in enumerate(agents):
        toolsets = [
            tool for tool in (agent.tools or []) if isinstance(tool, McpToolset)
        ]
        if index == evidence_index:
            assert len(toolsets) == 1
        else:
            assert toolsets == []


def test_phase2_pipeline_factory_never_reuses_parented_agents() -> None:
    first = create_phase2_pipeline()
    second = create_phase2_pipeline()

    assert first is not second
    assert len(first.sub_agents) == len(second.sub_agents)
    assert all(
        first_agent is not second_agent
        for first_agent, second_agent in zip(
            first.sub_agents,
            second.sub_agents,
            strict=True,
        )
    )
