"""Verify Parallel MCP connectivity without invoking a search or model."""

from __future__ import annotations

import asyncio
import os

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

REQUIRED_TOOLS = {"web_search", "web_fetch"}


async def probe_parallel_mcp(url: str) -> tuple[str, ...]:
    """Connect to Parallel MCP and return advertised tool names only."""

    async with streamable_http_client(url) as streams:
        read_stream, write_stream = streams[0], streams[1]
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()
            return tuple(sorted(tool.name for tool in result.tools))


async def _main() -> int:
    url = os.getenv("PARALLEL_MCP_URL", "https://search.parallel.ai/mcp")
    try:
        tools = await asyncio.wait_for(probe_parallel_mcp(url), timeout=45)
    except Exception as exc:  # noqa: BLE001 - CLI must report transport failures clearly.
        print("PARALLEL_MCP_CONNECTIVITY=FAIL")
        print(f"ERROR={type(exc).__name__}: {exc}")
        return 1

    missing = REQUIRED_TOOLS.difference(tools)
    if missing:
        print("PARALLEL_MCP_CONNECTIVITY=FAIL")
        print("MISSING_TOOLS=" + ",".join(sorted(missing)))
        print("ADVERTISED_TOOLS=" + ",".join(tools))
        return 1

    print("PARALLEL_MCP_CONNECTIVITY=PASS")
    print("ADVERTISED_TOOLS=" + ",".join(tools))
    print("TOOL_INVOCATIONS=0")
    print("GEMINI_CALLS=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main()))
