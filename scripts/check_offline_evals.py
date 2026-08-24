"""Validate the controlled CineScout evaluation corpus at no cost."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_CORPUS = REPO_ROOT / "evals" / "scenarios.json"


def _load_scenarios():
    """Load repository evaluation scenarios from a standalone script invocation."""

    repo_root = str(REPO_ROOT)
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from app.evaluation import load_scenarios

    return load_scenarios(EVALUATION_CORPUS)


def main() -> int:
    scenarios = _load_scenarios()
    categories = Counter(
        category.value
        for scenario in scenarios
        for category in scenario.expected_research_categories
    )

    print(f"OFFLINE_EVALUATION_SCENARIOS={len(scenarios)}")
    print("OFFLINE_EVALUATION_CATEGORIES=" + ",".join(sorted(categories)))
    print("PRE_CREDIT_EVALUATION_CONTRACT=PASS")
    print("LIVE_MODEL_CALLS=0")
    print("EXTERNAL_SEARCH_CALLS=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
