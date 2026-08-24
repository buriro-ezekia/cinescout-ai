"""Runtime configuration for CineScout AI."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Environment-backed settings used by the Phase 1 agent."""

    model: str = os.getenv("CINESCOUT_MODEL", "gemini-3.6-flash")
    parallel_mcp_url: str = os.getenv(
        "PARALLEL_MCP_URL", "https://search.parallel.ai/mcp"
    )
    parallel_api_key: str | None = os.getenv("PARALLEL_API_KEY") or None


settings = Settings()
