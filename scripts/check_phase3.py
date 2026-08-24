"""Validate CineScout AI Phase 3 resilience fixtures without live external calls."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.phase3.contracts import REQUIRED_RESILIENCE_PROPERTIES  # noqa: E402
from app.phase3.validation import (  # noqa: E402
    load_resilience_scenarios,
    validate_resilience_corpus,
)


def main() -> int:
    """Check deterministic Phase 3 resilience expectations."""

    scenarios = load_resilience_scenarios()
    failures = validate_resilience_corpus(scenarios)
    valid_controls = sum(bool(scenario["expected_valid"]) for scenario in scenarios)
    expected_failures = len(scenarios) - valid_controls

    if failures:
        print("PHASE3_RESILIENCE_CONTRACT=FAIL")
        for failure in failures:
            print(f"PHASE3_FAILURE={failure}")
        return 1

    print(f"PHASE3_RESILIENCE_SCENARIOS={len(scenarios)}")
    print(f"PHASE3_VALID_CONTROLS={valid_controls}")
    print(f"PHASE3_EXPECTED_FAILURE_CASES={expected_failures}")
    print("PHASE3_PROPERTIES=" + ",".join(sorted(REQUIRED_RESILIENCE_PROPERTIES)))
    print("PHASE3_MALFORMED_STATE_REJECTION=PASS")
    print("PHASE3_EMPTY_PLAN_HANDLING=PASS")
    print("PHASE3_UNSUPPORTED_CLAIM_HANDLING=PASS")
    print("PHASE3_CONFLICT_HANDLING=PASS")
    print("PHASE3_CONFIDENCE_NON_ESCALATION=PASS")
    print("PHASE3_SOURCE_PRESERVATION=PASS")
    print("PHASE3_UNCERTAINTY_PROPAGATION=PASS")
    print("PHASE3_BUDGET_ENFORCEMENT=PASS")
    print("PHASE3_FINAL_REPORT_CONTRACT=PASS")
    print("PHASE3_GEMINI_CALLS=0")
    print("PHASE3_EXTERNAL_SEARCH_CALLS=0")
    print("PHASE3_RESILIENCE_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
