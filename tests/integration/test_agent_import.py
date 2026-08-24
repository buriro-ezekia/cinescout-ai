"""Import-level integration tests for the ADK application."""

from importlib.metadata import version

import pytest

pytest.importorskip("google.adk")


def test_supported_mcp_toolset_import_path() -> None:
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

    assert McpToolset.__name__ == "McpToolset"


def test_adk_version_matches_phase1_pin() -> None:
    assert version("google-adk") == "2.7.1"


def test_adk_application_imports() -> None:
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

    from app.agent import app, parallel_search, root_agent

    assert root_agent.name == "cinescout_phase1"
    assert app.name == "app"
    assert isinstance(parallel_search, McpToolset)
