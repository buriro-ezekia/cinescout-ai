"""Repository-level contract tests for the Phase 1 vertical slice."""

from pathlib import Path


def test_phase1_spec_contains_acceptance_criteria() -> None:
    spec = Path(".agents-cli-spec.md").read_text(encoding="utf-8")
    assert "Phase 1 acceptance criteria" in spec
    assert "Parallel Search MCP" in spec
    assert "No secrets" in spec


def test_agent_declares_parallel_mcp_tools() -> None:
    source = Path("app/agent.py").read_text(encoding="utf-8")
    assert "McpToolset" in source
    assert 'tool_filter=["web_search", "web_fetch"]' in source
    assert "parallel_search" in source
