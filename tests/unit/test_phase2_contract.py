"""Repository contracts for the CineScout AI Phase 2 specialist workflow."""

import subprocess
import sys
from pathlib import Path

from app.contracts import REQUIRED_RESPONSE_SECTIONS
from app.phase2.contracts import (
    MAX_RESEARCH_TASKS,
    MAX_WEB_FETCH_CALLS,
    MAX_WEB_SEARCH_CALLS,
    PHASE2_STAGE_ORDER,
    PHASE2_STAGES,
    SpecialistRole,
)
from app.phase2.prompts import (
    EVIDENCE_VERIFIER_INSTRUCTION,
    REPORT_SYNTHESISER_INSTRUCTION,
    RESEARCH_PLANNER_INSTRUCTION,
)


def _normalise_whitespace(value: str) -> str:
    """Collapse formatting whitespace for semantic prompt-contract assertions."""

    return " ".join(value.split())


def test_phase2_stage_order_and_state_keys_are_stable() -> None:
    assert PHASE2_STAGE_ORDER == (
        SpecialistRole.BRIEF_INTERPRETER,
        SpecialistRole.RESEARCH_PLANNER,
        SpecialistRole.EVIDENCE_VERIFIER,
        SpecialistRole.PRODUCTION_RISK,
        SpecialistRole.REPORT_SYNTHESISER,
    )

    output_keys = tuple(stage.output_key for stage in PHASE2_STAGES)
    assert output_keys == (
        "phase2_brief_analysis",
        "phase2_research_plan",
        "phase2_evidence_review",
        "phase2_risk_assessment",
        "phase2_final_report",
    )
    assert len(output_keys) == len(set(output_keys))


def test_only_evidence_verifier_owns_parallel_boundary() -> None:
    parallel_roles = tuple(stage.role for stage in PHASE2_STAGES if stage.uses_parallel)
    assert parallel_roles == (SpecialistRole.EVIDENCE_VERIFIER,)


def test_phase2_research_budget_is_bounded() -> None:
    assert MAX_RESEARCH_TASKS == 6
    assert MAX_WEB_SEARCH_CALLS == 6
    assert MAX_WEB_FETCH_CALLS == 3

    planner = _normalise_whitespace(RESEARCH_PLANNER_INSTRUCTION)
    verifier = _normalise_whitespace(EVIDENCE_VERIFIER_INSTRUCTION)

    assert f"no more than {MAX_RESEARCH_TASKS} research tasks" in planner
    assert f"no more than {MAX_WEB_SEARCH_CALLS} web_search calls" in verifier
    assert f"no more than {MAX_WEB_FETCH_CALLS} web_fetch calls" in verifier


def test_phase2_state_handoffs_are_explicit_in_prompts() -> None:
    assert "{phase2_brief_analysis}" in RESEARCH_PLANNER_INSTRUCTION
    assert "{phase2_research_plan}" in EVIDENCE_VERIFIER_INSTRUCTION
    assert "{phase2_brief_analysis}" in REPORT_SYNTHESISER_INSTRUCTION
    assert "{phase2_research_plan}" in REPORT_SYNTHESISER_INSTRUCTION
    assert "{phase2_evidence_review}" in REPORT_SYNTHESISER_INSTRUCTION
    assert "{phase2_risk_assessment}" in REPORT_SYNTHESISER_INSTRUCTION


def test_report_synthesiser_preserves_response_contract_order() -> None:
    positions = [
        REPORT_SYNTHESISER_INSTRUCTION.index(section)
        for section in REQUIRED_RESPONSE_SECTIONS
    ]
    assert positions == sorted(positions)


def test_phase1_default_entrypoint_remains_phase1() -> None:
    source = Path("app/agent.py").read_text(encoding="utf-8")
    assert 'name="cinescout_phase1"' in source
    assert "app.phase2" not in source


def test_phase2_uses_graph_workflow_not_deprecated_sequential_agent() -> None:
    source = Path("app/phase2/agent.py").read_text(encoding="utf-8")

    assert "Workflow" in source
    assert "SequentialAgent" not in source
    assert 'mode="single_turn"' in source
    assert 'include_contents="none"' in source


def test_phase2_check_runs_outside_repository_root(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[2]
    script = repository_root / "scripts" / "check_phase2.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "PHASE2_ORCHESTRATOR=Workflow" in result.stdout
    assert "PHASE2_SPECIALISTS=5" in result.stdout
    assert "PHASE2_PARALLEL_OWNER=evidence_verifier" in result.stdout
    assert "PHASE2_AGENT_ISOLATION=PASS" in result.stdout
    assert "PHASE2_GEMINI_CALLS=0" in result.stdout
    assert "PHASE2_EXTERNAL_SEARCH_CALLS=0" in result.stdout
    assert "PHASE2_OFFLINE_CONTRACT=PASS" in result.stdout
