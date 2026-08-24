"""Repository boundaries for CineScout AI Phase 3 resilience evaluation."""

from pathlib import Path


def test_phase3_spec_and_fixture_corpus_exist() -> None:
    spec = Path("docs/phase3-spec.md")
    corpus = Path("evals/resilience_scenarios.json")

    assert spec.is_file()
    assert corpus.is_file()
    assert "Phase 3" in spec.read_text(encoding="utf-8")


def test_phase3_does_not_modify_runtime_entrypoints() -> None:
    phase1 = Path("app/agent.py").read_text(encoding="utf-8")
    phase2 = Path("app/phase2/agent.py").read_text(encoding="utf-8")

    assert "app.phase3" not in phase1
    assert "app.phase3" not in phase2
    assert 'name="cinescout_phase1"' in phase1
    assert 'name="cinescout_phase2_pipeline"' in phase2


def test_phase3_checker_cannot_execute_models_or_partner_tools() -> None:
    source = Path("scripts/check_phase3.py").read_text(encoding="utf-8")

    assert "Runner(" not in source
    assert ".run_async" not in source
    assert "call_tool(" not in source
    assert "google.adk" not in source
    assert 'print("PHASE3_GEMINI_CALLS=0")' in source
    assert 'print("PHASE3_EXTERNAL_SEARCH_CALLS=0")' in source


def test_phase3_is_wired_into_local_and_ci_readiness() -> None:
    local = Path("scripts/local_readiness.ps1").read_text(encoding="utf-8")
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "python scripts/check_phase3.py" in local
    assert "PHASE3_RESILIENCE_READINESS=PASS" in local
    assert "python scripts/check_phase3.py" in ci
