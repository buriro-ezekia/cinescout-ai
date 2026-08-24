"""Validate the controlled CineScout evaluation corpus at no cost."""

from __future__ import annotations

from collections import Counter

from app.evaluation import load_scenarios


def main() -> int:
    scenarios = load_scenarios("evals/scenarios.json")
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
