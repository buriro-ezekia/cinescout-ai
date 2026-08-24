"""Safeguards for development before Google hackathon credits are available."""

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
