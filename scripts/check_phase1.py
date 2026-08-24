"""Perform a fast readiness check for the Phase 1 repository at no cost."""

from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

REQUIRED_FILES = [
    ".agents-cli-spec.md",
    "agents-cli-manifest.yaml",
    "app/agent.py",
    "app/config.py",
    "app/contracts.py",
    "app/evaluation.py",
    "app/prompts.py",
    "docs/pre-credit-hardening.md",
    "evals/scenarios.json",
    "scripts/check_offline_evals.py",
    "scripts/check_parallel_mcp.py",
    "tests/unit/test_configuration.py",
    "tests/unit/test_evaluation_contract.py",
    "tests/unit/test_precredit_safeguards.py",
    "README.md",
    "LICENSE",
]

EXPECTED_PACKAGES = {
    "google-adk": "2.7.1",
    "mcp": "1.29.0",
}


def _check_packages() -> bool:
    ok = True
    for package, expected in EXPECTED_PACKAGES.items():
        try:
            installed = version(package)
        except PackageNotFoundError:
            print(f"PACKAGE_MISSING={package}")
            ok = False
            continue

        print(f"{package.upper().replace('-', '_')}_VERSION={installed}")
        if installed != expected:
            print(f"PACKAGE_VERSION_MISMATCH={package}:expected={expected}:installed={installed}")
            ok = False
    return ok


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not Path(path).exists()]
    packages_ok = _check_packages()

    if missing or not packages_ok:
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
