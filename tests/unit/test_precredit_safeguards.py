"""Safeguards for development before Google hackathon credits are available."""

import subprocess
import sys
from pathlib import Path


def test_parallel_probe_does_not_invoke_tools() -> None:
    source = Path("scripts/check_parallel_mcp.py").read_text(encoding="utf-8")

    assert "list_tools()" in source
    assert "call_tool(" not in source
    assert 'print("TOOL_INVOCATIONS=0")' in source
    assert 'print("GEMINI_CALLS=0")' in source


def test_offline_evaluation_check_declares_zero_external_calls() -> None:
    source = Path("scripts/check_offline_evals.py").read_text(encoding="utf-8")

    assert 'print("LIVE_MODEL_CALLS=0")' in source
    assert 'print("EXTERNAL_SEARCH_CALLS=0")' in source


def test_phase2_offline_check_cannot_execute_agents_or_tools() -> None:
    source = Path("scripts/check_phase2.py").read_text(encoding="utf-8")

    assert "call_tool(" not in source
    assert "Runner(" not in source
    assert ".run_async" not in source
    assert 'print("PHASE2_GEMINI_CALLS=0")' in source
    assert 'print("PHASE2_EXTERNAL_SEARCH_CALLS=0")' in source


def test_offline_evaluation_entrypoint_runs_outside_repository_root(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[2]
    script = repository_root / "scripts" / "check_offline_evals.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "OFFLINE_EVALUATION_SCENARIOS=6" in result.stdout
    assert "PRE_CREDIT_EVALUATION_CONTRACT=PASS" in result.stdout
    assert "LIVE_MODEL_CALLS=0" in result.stdout
    assert "EXTERNAL_SEARCH_CALLS=0" in result.stdout
