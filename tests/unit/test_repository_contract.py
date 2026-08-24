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


def test_local_readiness_enforces_isolated_supported_environment() -> None:
    source = Path("scripts/local_readiness.ps1").read_text(encoding="utf-8")
    assert "$env:VIRTUAL_ENV" in source
    assert "$LASTEXITCODE -ne 0" in source
    assert 'Version -ge [version]"3.14"' in source
    assert "PHASE1_LOCAL_READINESS=PASS" in source
