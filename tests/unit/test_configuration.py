"""No-cost unit checks for Phase 1 configuration and evidence guardrails."""

from pathlib import Path


def test_parallel_mcp_defaults_to_official_search_endpoint() -> None:
    source = Path("app/config.py").read_text(encoding="utf-8")
    assert "https://search.parallel.ai/mcp" in source


def test_prompt_requires_external_verification() -> None:
    prompt = Path("app/prompts.py").read_text(encoding="utf-8").lower()
    assert "use the parallel web_search tool" in prompt
    assert "never invent a source" in prompt
    assert "verified" in prompt
    assert "uncertainty" in prompt


def test_environment_template_does_not_contain_a_real_secret() -> None:
    content = Path(".env.example").read_text(encoding="utf-8")
    assert "PARALLEL_API_KEY=\n" in content
    assert "your-google-cloud-project-id" in content
