"""Import-level integration tests for the ADK application."""

from importlib.metadata import version

import pytest
from packaging.version import Version

pytest.importorskip("google.adk")
pytest.importorskip("mcp")


def test_supported_mcp_toolset_import_path() -> None:
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

    assert McpToolset.__name__ == "McpToolset"


def test_adk_and_mcp_versions_match_phase1_baseline() -> None:
    assert version("google-adk") == "2.7.1"
    mcp_version = Version(version("mcp"))
    assert Version("1.24.0") <= mcp_version < Version("2.0.0")


def test_adk_application_imports() -> None:
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

    from app.agent import app, parallel_search, root_agent

    assert root_agent.name == "cinescout_phase1"
    assert app.name == "app"
    assert isinstance(parallel_search, McpToolset)
