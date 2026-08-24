# CineScout AI

**Evidence-backed agentic pre-production research for filmmakers, producers and screenwriters.**

CineScout AI is being developed for the **Agentic Cinema: The Blockbuster Hackathon**. The project addresses a practical pre-production problem: creative teams often need to verify historical details, cultural context, locations, props, terminology and other production-sensitive claims across fragmented sources before they can make confident decisions.

Rather than behaving as a general film chatbot, CineScout turns a production brief or screenplay extract into a research task, uses external evidence where factual verification is required, and returns a concise production intelligence response that makes uncertainty visible.

## Phase 1 status

Phase 1 implements the project's first complete vertical slice:

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

The purpose of this phase is deliberately narrow. Before introducing several specialist agents, the repository first proves that Gemini can reason about a production brief, invoke the required partner service at runtime, receive live evidence and use that evidence in the final response.

## Technology

- **Google Agent Development Kit (ADK)** for the agent runtime;
- **Gemini** as the reasoning model;
- **Google Cloud / Vertex AI** as the intended hackathon runtime;
- **Parallel Search MCP** for live web research and evidence retrieval;
- **Agents CLI** for local development, evaluation and later deployment support;
- **GitHub Actions** for no-secret, no-paid-call quality checks.

Parallel's Search MCP supports anonymous light usage, so a Parallel API key is not required for the initial local vertical slice. A key can be supplied later if higher rate limits are needed.

## What the Phase 1 agent does

Given a screenplay extract or production brief, the agent is instructed to:

1. identify factual or contextual matters that require external verification;
2. use Parallel `web_search` for claims that depend on external evidence;
3. use `web_fetch` when a particular source needs closer inspection;
4. distinguish evidence from interpretation and recommendation;
5. make conflicting or insufficient evidence explicit; and
6. explain the practical production implications of what it found.

It must not invent sources or present uncertain material as verified fact.

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

The project is intended to run comfortably from a local VS Code terminal. Codespaces are not required.

### 1. Use Python 3.11, 3.12 or 3.13

Python 3.12 is recommended for the hackathon development environment.

From PowerShell in the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### 2. Create the local environment file

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set your Google Cloud project. The recommended configuration is:

```text
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
CINESCOUT_MODEL=gemini-3.6-flash
PARALLEL_MCP_URL=https://search.parallel.ai/mcp
```

Do not commit `.env` or service-account credentials.

### 3. Authenticate to Google Cloud

For local Vertex AI development, use Application Default Credentials:

```powershell
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

The relevant Vertex AI APIs must be enabled in the selected Google Cloud project.

### 4. Run the no-cost readiness suite

```powershell
powershell -ExecutionPolicy Bypass -File scripts\local_readiness.ps1
```

This performs compilation, linting, automated tests and repository-contract checks. It deliberately avoids live Gemini and Parallel calls.

A successful run ends with:

```text
PHASE1_LOCAL_READINESS=PASS
```

### 5. Run the agent locally

Install the current Google Agents CLI if it is not already available:

```powershell
python -m pip install google-agents-cli
```

Then run a terminal smoke test:

```powershell
agents-cli run "A historical drama is set in Zanzibar in 1962. A scene shows a specific vehicle model, refers to a public institution by name, and uses a period political term. Identify which details require verification, research them, and explain any production risks with sources."
```

For an interactive local interface:

```powershell
agents-cli playground
```

The playground is normally available at `http://localhost:8080`.

## What to verify during the first live test

The first credentialled run should demonstrate four things:

- Gemini receives and interprets the production brief;
- the agent invokes Parallel Search MCP rather than answering externally verifiable claims from memory alone;
- the response identifies its evidence and uncertainty; and
- the final answer explains why the evidence matters to the production decision.

That live run is the final manual acceptance check for Phase 1.

## Cost discipline

The repository is designed so that ordinary CI does not make live model or partner-service calls. This prevents test runs from consuming cloud credits. Parallel Search MCP can be used anonymously for light usage; Google model calls should be limited to deliberate local smoke tests during this phase.

## Security

Secrets do not belong in source control. The repository ignores `.env`, local virtual environments, service-account JSON files and common generated artefacts. Production credentials will later move to Google Secret Manager and workload identity rather than repository variables or committed files.

## Next development phase

Once the vertical slice has been reproduced successfully from a clean clone, the next phase will separate the current root workflow into specialist agents for brief interpretation, research planning, evidence verification, production-risk assessment and report synthesis. The existing Parallel MCP integration will remain the shared research foundation.

## Licence

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
