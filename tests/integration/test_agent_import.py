"""Import-level integration test for the ADK application."""

import pytest

pytest.importorskip("google.adk")


def test_adk_application_imports() -> None:
    from app.agent import app, root_agent

    assert root_agent.name == "cinescout_phase1"
    assert app.name == "app"
