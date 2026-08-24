"""Import-level integration tests for the Phase 2 ADK candidate."""

import pytest

pytest.importorskip("google.adk")

from google.adk import START, Workflow
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from app.phase2.agent import (
    create_phase2_pipeline,
    create_phase2_specialists,
    phase2_app,
    phase2_root_agent,
)
from app.phase2.contracts import PHASE2_STAGES, SpecialistRole


def test_phase2_application_imports_without_live_calls() -> None:
    assert isinstance(phase2_root_agent, Workflow)
    assert phase2_root_agent.name == "cinescout_phase2_pipeline"
    assert phase2_app.name == "phase2_app"


def test_phase2_pipeline_matches_specialist_contract() -> None:
    specialists = create_phase2_specialists()

    assert len(specialists) == 5
    assert tuple(agent.name for agent in specialists) == tuple(
        stage.agent_name for stage in PHASE2_STAGES
    )
    assert tuple(agent.output_key for agent in specialists) == tuple(
        stage.output_key for stage in PHASE2_STAGES
    )


def test_phase2_workflow_contains_exact_sequential_graph() -> None:
    pipeline = create_phase2_pipeline()

    assert pipeline.graph is not None
    actual_edges = tuple(
        (edge.from_node.name, edge.to_node.name) for edge in pipeline.graph.edges
    )
    expected_names = tuple(stage.agent_name for stage in PHASE2_STAGES)
    expected_edges = tuple(
        zip(
            (START.name, *expected_names[:-1]),
            expected_names,
            strict=True,
        )
    )

    assert actual_edges == expected_edges


def test_only_evidence_verifier_has_parallel_toolset() -> None:
    specialists = create_phase2_specialists()
    evidence_index = next(
        index
        for index, stage in enumerate(PHASE2_STAGES)
        if stage.role is SpecialistRole.EVIDENCE_VERIFIER
    )

    for index, agent in enumerate(specialists):
        toolsets = [
            tool for tool in (agent.tools or []) if isinstance(tool, McpToolset)
        ]
        if index == evidence_index:
            assert len(toolsets) == 1
        else:
            assert toolsets == []


def test_phase2_specialists_are_explicitly_isolated_single_turn_nodes() -> None:
    specialists = create_phase2_specialists()

    assert all(agent.mode == "single_turn" for agent in specialists)
    assert all(agent.include_contents == "none" for agent in specialists)


def test_phase2_factory_creates_fresh_specialist_nodes() -> None:
    first = create_phase2_specialists()
    second = create_phase2_specialists()

    assert len(first) == len(second) == 5
    assert all(
        first_agent is not second_agent
        for first_agent, second_agent in zip(first, second, strict=True)
    )
