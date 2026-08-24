"""Tool factories for the CineScout AI Phase 2 candidate."""

from __future__ import annotations

from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset

from app.config import settings


def _parallel_headers() -> dict[str, str]:
    """Return optional Parallel authentication headers."""

    if not settings.parallel_api_key:
        return {}
    return {"Authorization": f"Bearer {settings.parallel_api_key}"}


def create_parallel_search_toolset() -> McpToolset:
    """Create a fresh Parallel MCP toolset for one specialist-agent graph."""

    return McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=settings.parallel_mcp_url,
            headers=_parallel_headers(),
            timeout=30,
            sse_read_timeout=60,
        ),
        tool_filter=["web_search", "web_fetch"],
    )
