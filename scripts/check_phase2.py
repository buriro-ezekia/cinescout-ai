"""Validate the CineScout AI Phase 2 candidate without live external calls."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from google.adk import START, Workflow  # noqa: E402
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset  # noqa: E402

from app.phase2.agent import (  # noqa: E402
    create_phase2_pipeline,
    create_phase2_specialists,
)
from app.phase2.contracts import PHASE2_STAGES, SpecialistRole  # noqa: E402


def main() -> int:
    """Check Phase 2 orchestration and tool ownership without executing agents."""

    pipeline = create_phase2_pipeline()
    specialists = create_phase2_specialists()
    second_specialists = create_phase2_specialists()

    expected_names = tuple(stage.agent_name for stage in PHASE2_STAGES)
    expected_keys = tuple(stage.output_key for stage in PHASE2_STAGES)
    actual_names = tuple(agent.name for agent in specialists)
    actual_keys = tuple(agent.output_key for agent in specialists)

    parallel_owners = []
    for stage, agent in zip(PHASE2_STAGES, specialists, strict=True):
        tools = agent.tools or []
        if any(isinstance(tool, McpToolset) for tool in tools):
            parallel_owners.append(stage.role)

    fresh_specialists = all(
        first is not second
        for first, second in zip(
            specialists,
            second_specialists,
            strict=True,
        )
    )
    isolated_specialists = all(
        agent.mode == "single_turn" and agent.include_contents == "none"
        for agent in specialists
    )

    expected_edges = tuple(
        zip(
            (START.name, *expected_names[:-1]),
            expected_names,
            strict=True,
        )
    )
    actual_edges: tuple[tuple[str, str], ...] = ()
    if pipeline.graph is not None:
        actual_edges = tuple(
            (edge.from_node.name, edge.to_node.name) for edge in pipeline.graph.edges
        )

    checks = (
        isinstance(pipeline, Workflow),
        len(specialists) == 5,
        actual_names == expected_names,
        actual_keys == expected_keys,
        actual_edges == expected_edges,
        tuple(parallel_owners) == (SpecialistRole.EVIDENCE_VERIFIER,),
        fresh_specialists,
        isolated_specialists,
    )

    if not all(checks):
        print("PHASE2_OFFLINE_CONTRACT=FAIL")
        print("PHASE2_STAGE_ORDER=" + ",".join(actual_names))
        print("PHASE2_OUTPUT_KEYS=" + ",".join(str(key) for key in actual_keys))
        print("PHASE2_PARALLEL_OWNERS=" + ",".join(role.value for role in parallel_owners))
        print(f"PHASE2_ACTUAL_EDGES={actual_edges}")
        return 1

    print("PHASE2_ORCHESTRATOR=Workflow")
    print("PHASE2_SPECIALISTS=5")
    print("PHASE2_STAGE_ORDER=" + ",".join(stage.role.value for stage in PHASE2_STAGES))
    print("PHASE2_OUTPUT_KEYS=" + ",".join(expected_keys))
    print("PHASE2_PARALLEL_OWNER=evidence_verifier")
    print("PHASE2_GRAPH_CHAIN=PASS")
    print("PHASE2_FACTORY_ISOLATION=PASS")
    print("PHASE2_AGENT_ISOLATION=PASS")
    print("PHASE2_GEMINI_CALLS=0")
    print("PHASE2_EXTERNAL_SEARCH_CALLS=0")
    print("PHASE2_OFFLINE_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
