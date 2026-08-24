# CineScout AI

**Evidence-backed agentic pre-production research for filmmakers, producers and screenwriters.**

CineScout AI is being developed for the **Agentic Cinema: The Blockbuster Hackathon**. It addresses a practical pre-production challenge: creative teams often need to verify historical details, cultural context, locations, props, terminology and other production-sensitive claims across fragmented sources before making confident decisions.

Rather than operating as a general-purpose film assistant, CineScout turns a production brief or screenplay extract into a structured research task. It uses external evidence where factual verification is required and returns concise production intelligence that distinguishes evidence, interpretation, uncertainty and recommendation.

## Phase 1 status

Phase 1 establishes the project's first complete vertical slice:

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

This phase is intentionally focused. Before introducing several specialist agents, the repository first demonstrates that Gemini can interpret a production brief, invoke the required partner service at runtime, receive external evidence and use that evidence to support a practical production response.

## Technology

- **Google Agent Development Kit (ADK) 2.7.1** provides the agent runtime;
- **Gemini** provides the reasoning model;
- **Google Cloud / Vertex AI** is the intended hackathon runtime;
- **Parallel Search MCP** provides external web research and evidence retrieval;
- **Agents CLI** supports local development, evaluation and later deployment work;
- **GitHub Actions** provides quality checks without external credentials or live model calls.

The Phase 1 dependency baseline pins Google ADK to version `2.7.1`. This protects the current vertical slice from unreviewed SDK changes while the hackathon is in progress. The validated MCP toolset import is:

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
```

The development workflow is designed to remain **at no cost** during the hackathon by using the available Google Cloud credits for deliberate model testing and Parallel Search MCP's anonymous light-use allowance for the initial research workflow. A Parallel API key is therefore not required for the Phase 1 local vertical slice.

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
└── requirements-dev.txt
```

## Local development on Windows

The repository is designed for local development in VS Code. Codespaces are not required, which allows routine development and validation to remain at no cost apart from deliberate Google Cloud model calls covered by the hackathon credits.

### 1. Confirm a supported Python installation

The repository supports Python **3.11, 3.12 and 3.13**. Python **3.12 is recommended** for a stable and reproducible hackathon environment. Python 3.14 is not supported by the current repository configuration and should not be used for Phase 1 validation.

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

Install the development dependencies and verify their integrity:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip check
```

A successful `pip check` should report:

```text
No broken requirements found.
```

### 3. Create the local environment file

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set the Google Cloud project when the credentialled smoke test is required. The recommended configuration is:

```text
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
CINESCOUT_MODEL=gemini-3.6-flash
PARALLEL_MCP_URL=https://search.parallel.ai/mcp
```

Do not commit `.env`, access tokens or service-account credentials.

### 4. Run the Phase 1 readiness checks at no cost

```powershell
powershell -ExecutionPolicy Bypass -File scripts\local_readiness.ps1
```

The script performs five checks without making live Gemini or Parallel calls:

- dependency integrity with `pip check`;
- Python compilation;
- Ruff linting;
- automated tests; and
- the Phase 1 repository contract.

The script stops immediately if the Python version is unsupported, no virtual environment is active, a dependency is inconsistent, or any command returns a non-zero exit code. A successful run ends with:

```text
PHASE1_LOCAL_READINESS=PASS
```

A `PASS` therefore means that every local readiness check completed successfully.

### 5. Authenticate to Google Cloud for the deliberate live test

The automated readiness checks above run at no cost and require no Google Cloud credentials. Authentication is only required for the deliberate Gemini smoke test.

For local Vertex AI development, use Application Default Credentials:

```powershell
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

The relevant Vertex AI APIs must be enabled in the selected Google Cloud project.

### 6. Run the agent locally

Install Google Agents CLI if it is not already available in the active virtual environment:

```powershell
python -m pip install google-agents-cli
```

Run a terminal smoke test:

```powershell
agents-cli run "A historical drama is set in Zanzibar in 1962. A scene shows a specific vehicle model, refers to a public institution by name, and uses a period political term. Identify which details require verification, research them, and explain any production risks with sources."
```

For an interactive local interface:

```powershell
agents-cli playground
```

The playground is normally available at `http://localhost:8080`.

## Troubleshooting the ADK MCP import

Phase 1 is validated against Google ADK `2.7.1`. If an environment reports an error similar to:

```text
ImportError: cannot import name 'McpToolset' from 'google.adk.tools.mcp_tool'
```

first pull the latest repository changes, activate the project virtual environment, and reinstall the pinned dependencies:

```powershell
git pull
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pip check
```

The repository imports `McpToolset` from `google.adk.tools.mcp_tool.mcp_toolset`, which is the supported module path for the validated Phase 1 baseline.

## Phase 1 live acceptance check

The first credentialled run should demonstrate four things:

- Gemini receives and interprets the production brief;
- the agent invokes Parallel Search MCP for externally verifiable claims rather than relying on model memory alone;
- the response identifies its evidence and uncertainty; and
- the final response explains why the evidence matters to the production decision.

This deliberate live run is the remaining manual acceptance check for Phase 1. It should be used sparingly so that development remains at no cost within the hackathon's available credits and partner allowance.

## Development at no cost

Ordinary CI and local readiness checks do not make live model or partner-service calls. This prevents routine validation from consuming Google Cloud credits. Parallel Search MCP can be used for anonymous light usage, while Gemini calls are reserved for deliberate integration and demonstration tests covered by the available hackathon credits.

## Security

Secrets do not belong in source control. The repository ignores `.env`, local virtual environments, service-account JSON files and common generated artefacts. Production credentials will later be managed through Google Secret Manager and workload identity rather than committed files.

## Next development phase

Once the vertical slice has been reproduced successfully from a clean local clone, the next phase will separate the current root workflow into specialist agents for brief interpretation, research planning, evidence verification, production-risk assessment and report synthesis. The existing Parallel MCP integration will remain the shared research foundation.

## Licence

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
