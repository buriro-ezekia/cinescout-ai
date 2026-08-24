"""Google ADK entry point for the CineScout AI Phase 1 vertical slice."""

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.genai import types

from app.config import settings
from app.prompts import ROOT_AGENT_INSTRUCTION


def _parallel_headers() -> dict[str, str]:
    """Return optional authentication headers for higher Parallel MCP rate limits."""
    if not settings.parallel_api_key:
        return {}
    return {"Authorization": f"Bearer {settings.parallel_api_key}"}


parallel_search = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=settings.parallel_mcp_url,
        headers=_parallel_headers(),
        timeout=30,
        sse_read_timeout=60,
    ),
    tool_filter=["web_search", "web_fetch"],
)

root_agent = Agent(
    name="cinescout_phase1",
    model=Gemini(
        model=settings.model,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description=(
        "Evidence-backed pre-production research assistant using Gemini and Parallel Search."
    ),
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[parallel_search],
)

app = App(
    root_agent=root_agent,
    name="app",
)
