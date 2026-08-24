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

This phase is intentionally focused. Before introducing specialist agents, the repository first demonstrates that Gemini can interpret a production brief, invoke the required partner service at runtime, receive external evidence and use that evidence to support a practical production response.

## Technology

- **Google Agent Development Kit (ADK) 2.7.1** provides the agent runtime;
- **MCP Python SDK 1.29.0** provides the Model Context Protocol client required by the ADK MCP toolset;
- **Gemini** provides the reasoning model;
- **Google Cloud / Vertex AI** is the intended hackathon runtime;
- **Parallel Search MCP** provides external web research and evidence retrieval;
- **Agents CLI** supports local development, evaluation and later deployment work;
- **GitHub Actions** provides quality checks without external credentials or live model calls.

The Phase 1 dependency baseline is deliberately pinned to **Google ADK 2.7.1** and **MCP Python SDK 1.29.0**. Google ADK requires its MCP integration extra for `McpToolset`; the repository therefore installs `google-adk[gcp,mcp]==2.7.1` and keeps the MCP SDK on the compatible 1.x line. This avoids the breaking changes introduced in MCP 2.x during the hackathon.

The validated MCP toolset import is:

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
```

The development workflow is designed to remain **at no cost** during the hackathon by reserving Google Cloud model calls for deliberate tests covered by the available hackathon credits and using Parallel Search MCP's anonymous light-use allowance for the initial research workflow.

## What the Phase 1 agent does

Given a screenplay extract or production brief, the agent is instructed to:

1. identify factual or contextual matters that require external verification;
2. use Parallel `web_search` for claims that depend on external evidence;
3. use `web_fetch` when a particular source requires closer inspection;
4. distinguish evidence from interpretation and recommendation;
5. make conflicting or insufficient evidence explicit; and
6. explain the practical production implications of the evidence found.

The agent must not invent sources or present uncertain material as verified fact.

## Repository structure

```text
cinescout-ai/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   └── prompts.py
├── docs/
│   └── phase1.md
├── scripts/
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

The repository is designed for local development in VS Code. Codespaces are not required, which allows routine development and validation to remain at no cost apart from deliberate model calls covered by the hackathon credits.

### 1. Confirm a supported Python installation

The repository supports Python **3.11, 3.12 and 3.13**. Python **3.12 is recommended** for a stable and reproducible hackathon environment. Python 3.14 is not used for Phase 1 validation.

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

The install must include:

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
- automated tests; and
- the Phase 1 repository contract.

It stops immediately if the Python environment is unsupported, no virtual environment is active, a dependency is missing or inconsistent, or any command returns a non-zero exit code. A successful run ends with:

```text
PHASE1_LOCAL_READINESS=PASS
```

A `PASS` therefore means that every local readiness check completed successfully.

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

Then rerun:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\local_readiness.ps1
```

## Google Cloud configuration

The automated readiness checks run at no cost and require no Google Cloud credentials. Authentication is only required for the deliberate live Gemini acceptance test.

Create the local environment file when that test is required:

```powershell
Copy-Item .env.example .env
```

The intended configuration is:

```text
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
CINESCOUT_MODEL=gemini-3.6-flash
PARALLEL_MCP_URL=https://search.parallel.ai/mcp
```

Do not commit `.env`, access tokens or service-account credentials.

For local Vertex AI authentication:

```powershell
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

## Phase 1 live acceptance check

The first credentialled run must demonstrate that:

- Gemini receives and interprets the production brief;
- the agent invokes Parallel Search MCP for externally verifiable claims rather than relying on model memory alone;
- the response identifies its evidence and uncertainty; and
- the final response explains why the evidence matters to the production decision.

This live run is performed only after local readiness passes and should be used sparingly so that development remains at no cost within the hackathon's available credits and partner allowance.

## Security

Secrets do not belong in source control. The repository ignores `.env`, local virtual environments, service-account JSON files and common generated artefacts. Production credentials will later be managed through Google Secret Manager and workload identity rather than committed files.

## Next development phase

Once the Phase 1 vertical slice has been reproduced successfully from a clean local clone, the next phase will separate the current root workflow into specialist agents for brief interpretation, research planning, evidence verification, production-risk assessment and report synthesis. The existing Parallel MCP integration will remain the shared research foundation.

## Licence

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
