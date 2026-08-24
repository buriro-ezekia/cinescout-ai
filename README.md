# CineScout AI

**Evidence-backed agentic pre-production research for filmmakers, producers and screenwriters.**

CineScout AI is being developed for the **Agentic Cinema: The Blockbuster Hackathon**. It addresses a practical pre-production challenge: creative teams often need to verify historical details, cultural context, locations, props, terminology and other production-sensitive claims across fragmented sources before making confident decisions.

Rather than operating as a general-purpose film assistant, CineScout converts a production brief or screenplay extract into a structured research task. It uses external evidence where factual verification is required and returns concise production intelligence that distinguishes evidence, interpretation, uncertainty and recommendation.

## Phase 1 status

Phase 1 establishes the first complete vertical slice:

```text
Production brief
      |
      v
Gemini on Google ADK
      |
      v
Parallel Search MCP
      |
      v
External evidence
      |
      v
Evidence-backed production intelligence
```

The local Phase 1 baseline is now validated with Python 3.12, Google ADK 2.7.1 and MCP Python SDK 1.29.0. Dependency integrity, compilation, Ruff, the automated test suite and the repository contract pass locally.

The final Phase 1 acceptance condition is a credentialled Gemini → Parallel runtime test. That live test is intentionally deferred until Google Cloud hackathon credits are available for a dedicated CineScout AI project. Routine development therefore continues at no cost without using an unrelated production billing account.

## Technology

- **Google Agent Development Kit (ADK) 2.7.1** provides the agent runtime;
- **MCP Python SDK 1.29.0** provides the Model Context Protocol client required by the ADK MCP toolset;
- **Gemini** provides the reasoning model for the eventual credentialled runtime;
- **Google Cloud / Vertex AI** is the intended hackathon runtime;
- **Parallel Search MCP** provides external web research and evidence retrieval;
- **Agents CLI** supports local development, evaluation and later deployment work;
- **GitHub Actions** provides credential-free quality checks without live model or search calls.

The Phase 1 dependency baseline is deliberately pinned to **Google ADK 2.7.1** and **MCP Python SDK 1.29.0**. The repository installs `google-adk[gcp,mcp]==2.7.1` and keeps the MCP SDK on the validated 1.x line.

The validated MCP toolset import is:

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
```

## What the Phase 1 agent does

Given a screenplay extract or production brief, the agent is instructed to:

1. identify factual or contextual matters that require external verification;
2. use Parallel `web_search` for claims that depend on external evidence;
3. use `web_fetch` when a particular source requires closer inspection;
4. distinguish evidence from interpretation and recommendation;
5. make conflicting or insufficient evidence explicit; and
6. explain the practical production implications of the evidence found.

The agent must not invent sources or present uncertain material as verified fact.

## Pre-credit hardening at no cost

While Google Cloud hackathon credits are pending, the repository continues to progress through deterministic engineering work that does not require Gemini or Vertex AI requests.

The pre-credit hardening layer provides:

- typed production-research categories and evidence-status contracts;
- a controlled evaluation corpus covering historical, cultural, location, institutional, prop, terminology, logistics and rights-context research;
- deterministic checks for the required final-response structure;
- local and CI validation with zero Gemini calls and zero external search calls; and
- an optional manual Parallel MCP connectivity probe that lists server tools without invoking `web_search` or `web_fetch`.

The evaluation corpus does not attempt to manufacture research answers offline. Its purpose is to define what the later live agent must recognise and how evidence-backed output must be structured.

See [`docs/pre-credit-hardening.md`](docs/pre-credit-hardening.md) for the engineering boundary.

## Repository structure

```text
cinescout-ai/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── contracts.py
│   ├── evaluation.py
│   └── prompts.py
├── docs/
│   ├── phase1.md
│   └── pre-credit-hardening.md
├── evals/
│   └── scenarios.json
├── scripts/
│   ├── check_offline_evals.py
│   ├── check_parallel_mcp.py
│   ├── check_phase1.py
│   └── local_readiness.ps1
├── tests/
│   ├── integration/
│   └── unit/
├── .github/workflows/ci.yml
├── .vscode/mcp.json
├── .agents-cli-spec.md
├── .env.example
├── agents-cli-manifest.yaml
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## Local development on Windows

The repository is designed for local development in VS Code. Codespaces are not required, allowing routine development and validation to remain at no cost.

### 1. Confirm a supported Python installation

The repository supports Python **3.11, 3.12 and 3.13**. Python **3.12 is recommended** for the validated hackathon environment. Python 3.14 is not used for Phase 1 validation.

Check the Python installations detected by the Windows launcher:

```powershell
py --list
```

If Python 3.12 is not listed, it can be installed at no cost through Windows Package Manager:

```powershell
winget install -e --id Python.Python.3.12
```

Close and reopen the VS Code terminal after installation, then confirm:

```powershell
py -3.12 --version
```

### 2. Create and activate an isolated virtual environment

From PowerShell in the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

The final command should report Python 3.12.x. The readiness script requires an active virtual environment so that project dependencies remain isolated from the user's global Python environment.

Install or refresh the validated dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements-dev.txt
python -m pip check
```

The dependency baseline includes:

```text
google-adk[gcp,mcp]==2.7.1
mcp==1.29.0
```

A successful dependency check should report:

```text
No broken requirements found.
```

### 3. Run the Phase 1 readiness checks at no cost

```powershell
powershell -ExecutionPolicy Bypass -File scripts\local_readiness.ps1
```

The script checks:

- dependency integrity with `pip check`;
- Python compilation;
- Ruff linting;
- the automated test suite;
- the offline evaluation contract; and
- the Phase 1 repository contract.

The offline evaluation check explicitly reports:

```text
LIVE_MODEL_CALLS=0
EXTERNAL_SEARCH_CALLS=0
```

A successful run ends with:

```text
PHASE1_LOCAL_READINESS=PASS
```

## Optional Parallel MCP connectivity check

Parallel Search MCP can be checked independently of Gemini. The manual probe opens an MCP session and confirms that the endpoint advertises `web_search` and `web_fetch`.

It does **not** invoke either tool and is deliberately excluded from CI.

Run:

```powershell
python scripts\check_parallel_mcp.py
```

A successful result includes:

```text
PARALLEL_MCP_CONNECTIVITY=PASS
TOOL_INVOCATIONS=0
GEMINI_CALLS=0
```

This provides useful partner-integration evidence at no cost while the Google Cloud live-model test remains deferred.

## Troubleshooting MCP dependency errors

If the test suite reports:

```text
ModuleNotFoundError: No module named 'mcp'
```

pull the latest `main`, activate the existing Python 3.12 virtual environment and refresh the dependency set:

```powershell
git pull
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade -r requirements-dev.txt
python -m pip check
```

Confirm the validated runtime versions:

```powershell
python -c "from importlib.metadata import version; print('google-adk', version('google-adk')); print('mcp', version('mcp'))"
```

Expected output:

```text
google-adk 2.7.1
mcp 1.29.0
```

## Google Cloud configuration

Automated readiness and pre-credit evaluation run at no cost and require no Google Cloud credentials. The credentialled Gemini acceptance test remains deferred until hackathon credits are available for a dedicated CineScout AI project.

When that condition is met, the intended local environment is:

```text
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-cinescout-project-id
GOOGLE_CLOUD_LOCATION=global
CINESCOUT_MODEL=gemini-3.6-flash
PARALLEL_MCP_URL=https://search.parallel.ai/mcp
```

Do not commit `.env`, access tokens or service-account credentials.

## Phase 1 live acceptance check

The eventual credentialled run must demonstrate that:

- Gemini receives and interprets the production brief;
- the agent invokes Parallel Search MCP for externally verifiable claims rather than relying on model memory alone;
- the response identifies its evidence and uncertainty; and
- the final response explains why the evidence matters to the production decision.

Until hackathon credits are available, this is the only Phase 1 acceptance condition intentionally left incomplete.

## Security

Secrets do not belong in source control. The repository ignores `.env`, local virtual environments, service-account JSON files and common generated artefacts. Production credentials will later be managed through Google Secret Manager and workload identity rather than committed files.

## Next development phase

After the live Phase 1 runtime path is demonstrated, the next phase will separate the current workflow into specialist agents for brief interpretation, research planning, evidence verification, production-risk assessment and report synthesis. The existing Parallel MCP integration and pre-credit evaluation contracts will remain shared foundations.

## Licence

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
