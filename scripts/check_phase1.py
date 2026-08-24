"""Perform a fast readiness check for the Phase 1 repository at no cost."""

from __future__ import annotations

import os
from pathlib import Path

REQUIRED_FILES = [
    ".agents-cli-spec.md",
    "agents-cli-manifest.yaml",
    "app/agent.py",
    "app/config.py",
    "app/prompts.py",
    "tests/unit/test_configuration.py",
    "README.md",
    "LICENSE",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not Path(path).exists()]
    if missing:
        print("PHASE1_REPOSITORY_CONTRACT=FAIL")
        for path in missing:
            print(f"MISSING={path}")
        return 1

    print("PHASE1_REPOSITORY_CONTRACT=PASS")
    print("PARALLEL_MCP_URL=" + os.getenv("PARALLEL_MCP_URL", "https://search.parallel.ai/mcp"))
    print("GOOGLE_CLOUD_PROJECT_SET=" + str(bool(os.getenv("GOOGLE_CLOUD_PROJECT"))).lower())
    print("LIVE_MODEL_TEST=NOT_RUN")
    print(
        "Reason: credentials and external calls are intentionally excluded "
        "from this at-no-cost check."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
