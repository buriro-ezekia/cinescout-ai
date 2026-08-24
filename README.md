# CineScout AI

**Evidence-backed agentic pre-production research for filmmakers, producers and screenwriters.**

CineScout AI is being developed for the **Agentic Cinema: The Blockbuster Hackathon**. It addresses a practical pre-production problem: creative teams often need to verify historical details, cultural context, locations, institutions, props, terminology, logistics and other production-sensitive claims across fragmented sources before making confident decisions.

Rather than operating as a general-purpose film assistant, CineScout converts a production brief or screenplay extract into auditable production intelligence. External evidence is used where factual verification is required, while the system is designed to keep evidence, interpretation, uncertainty and recommendation clearly separated.

## Current development status

The Phase 1 foundation is locally validated with Python 3.12, Google ADK 2.7.1 and MCP Python SDK 1.29.0. Dependency integrity, compilation, Ruff, automated tests, the controlled offline evaluation corpus, repository contracts and Parallel MCP connectivity have all been reproduced locally.

Parallel connectivity has been demonstrated against the configured MCP endpoint with `web_search` and `web_fetch` advertised while making zero tool invocations and zero Gemini calls.

The remaining Phase 1 acceptance condition is the credentialled Gemini → Parallel runtime proof. That test is intentionally deferred until Google hackathon credits are available for a dedicated CineScout AI Google Cloud project. CineScout therefore does not use an unrelated production billing account while the credits are pending.

Phase 2 is now being built on top of the proven Phase 1 foundation as a separate specialist-agent candidate. The Phase 1 `app/agent.py` entry point remains unchanged and continues to be the repository default until the later credentialled acceptance process is complete.

## Phase 1 foundation

The validated vertical slice is:

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

The Phase 1 agent is instructed to identify externally verifiable matters, use Parallel research where evidence is required, preserve uncertainty and return practical production implications with sources.

## Phase 2 specialist architecture

Phase 2 separates the workflow into five deterministic specialist stages:

```text
Production brief or screenplay extract
        |
        v
Brief Interpreter
        |
        | phase2_brief_analysis
        v
Research Planner
        |
        | phase2_research_plan
        v
Evidence Verifier  ----> Parallel Search MCP
        |
        | phase2_evidence_review
        v
Production Risk Agent
        |
        | phase2_risk_assessment
        v
Report Synthesiser
        |
        | phase2_final_report
        v
Evidence-backed production intelligence
```

Google ADK `SequentialAgent` provides deterministic orchestration because each stage depends on the state produced by the previous stage. Every specialist is created through a factory function so pipeline instances never reuse child agents that already belong to another parent.

Only the **Evidence Verifier** owns a Parallel MCP toolset. The Brief Interpreter and Research Planner cannot search externally; the Production Risk Agent and Report Synthesiser consume verified state rather than conducting additional research. This keeps partner usage observable and avoids unnecessary search calls.

The default Phase 2 research budget is deliberately bounded to a maximum of six research tasks, no more than one `web_search` per planned task and no more than three `web_fetch` calls unless broader research is explicitly requested.

The Phase 2 specification and acceptance criteria are documented in [`docs/phase2-spec.md`](docs/phase2-spec.md).

## Evidence and response contracts

CineScout uses shared research categories covering:

- historical context;
- cultural context;
- geography and location;
- institutions;
- props and technology;
- terminology;
- logistics; and
- rights context.

Evidence confidence is represented as `high`, `medium`, `low` or `insufficient_evidence`.

The final production intelligence response must retain the established five-section structure:

1. Production reading
2. Evidence and verification
3. Production implications
4. Uncertainty or conflicts
5. Sources consulted

No stage may invent a source, present unsupported material as verified, or strengthen the certainty of evidence received from an earlier stage.

## Technology

- **Google Agent Development Kit (ADK) 2.7.1** provides the agent runtime and workflow orchestration;
- **MCP Python SDK 1.29.0** provides the Model Context Protocol client required by the ADK MCP toolset;
- **Gemini** provides reasoning for the later credentialled runtime;
- **Google Cloud / Vertex AI** is the intended hackathon runtime;
- **Parallel Search MCP** provides external research and evidence retrieval;
- **Agents CLI** supports local development, evaluation and later deployment work; and
- **GitHub Actions** provides credential-free quality checks without live model or search calls.

The dependency baseline installs:

```text
google-adk[gcp,mcp]==2.7.1
mcp==1.29.0
```

## Development at no cost while credits are pending

The repository is deliberately structured so useful engineering can continue at no cost before the Google hackathon credits arrive. Routine validation makes zero Gemini calls and zero external search calls.

The current at-no-cost engineering layer includes:

- deterministic Phase 1 and Phase 2 repository contracts;
- a six-scenario evaluation corpus covering all eight research categories;
- structured specialist state hand-offs;
- Phase 2 orchestration and tool-ownership tests;
- factory-isolation tests for ADK child agents;
- response-structure and evidence guardrails; and
- an optional manual Parallel MCP connectivity probe that lists tools without invoking them.

See [`docs/pre-credit-hardening.md`](docs/pre-credit-hardening.md) for the pre-credit engineering boundary.

## Repository structure

```text
cinescout-ai/
├── app/
│   ├── agent.py                  # validated Phase 1 default entry point
│   ├── config.py
│   ├── contracts.py
│   ├── evaluation.py
│   ├── prompts.py
│   └── phase2/
│       ├── agent.py              # five-stage Phase 2 candidate
│       ├── contracts.py          # stage, state and budget contracts
│       ├── prompts.py            # specialist instructions
│       └── tools.py              # fresh Parallel MCP toolset factory
├── docs/
│   ├── phase1.md
│   ├── phase2-spec.md
│   └── pre-credit-hardening.md
├── evals/
│   └── scenarios.json
├── scripts/
│   ├── check_offline_evals.py
│   ├── check_parallel_mcp.py
│   ├── check_phase1.py
│   ├── check_phase2.py
│   └── local_readiness.ps1
├── tests/
│   ├── integration/
│   └── unit/
├── .github/workflows/ci.yml
├── .vscode/mcp.json
├── .agents-cli-spec.md
├── agents-cli-manifest.yaml
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## Local development on Windows

The repository is designed for local development in VS Code. Codespaces are not required.

### 1. Use the validated Python environment

The repository supports Python 3.11, 3.12 and 3.13. Python **3.12** is recommended for the validated hackathon environment.

```powershell
py -3.12 --version
```

Create the virtual environment if required:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install or refresh the development dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements-dev.txt
python -m pip check
```

A successful dependency check reports:

```text
No broken requirements found.
```

### 2. Run the complete local readiness suite

```powershell
powershell -ExecutionPolicy Bypass -File scripts\local_readiness.ps1
```

The readiness suite performs:

- dependency integrity checks;
- Python compilation;
- Ruff linting;
- the complete automated test suite;
- the offline evaluation contract;
- the Phase 1 repository contract; and
- the Phase 2 offline structural contract.

The Phase 2 contract performs no agent execution. It verifies the `SequentialAgent` structure, specialist order, state keys, Parallel ownership and factory isolation while explicitly reporting zero Gemini and external search calls.

A complete successful run ends with:

```text
PHASE1_LOCAL_READINESS=PASS
PHASE2_OFFLINE_READINESS=PASS
CINESCOUT_LOCAL_READINESS=PASS
```

### 3. Optional Parallel MCP connectivity check

The manual probe can confirm that the configured Parallel endpoint advertises `web_search` and `web_fetch` without invoking either tool:

```powershell
python scripts\check_parallel_mcp.py
```

A successful result includes:

```text
PARALLEL_MCP_CONNECTIVITY=PASS
TOOL_INVOCATIONS=0
GEMINI_CALLS=0
```

The connectivity probe is intentionally excluded from CI because automated validation should not require network access.

## Troubleshooting the validated dependency baseline

If the environment reports an MCP import failure, pull the latest `main`, activate the existing Python 3.12 virtual environment and refresh the dependencies:

```powershell
git pull
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade -r requirements-dev.txt
python -m pip check
```

Confirm the pinned runtime versions:

```powershell
python -c "from importlib.metadata import version; print('google-adk', version('google-adk')); print('mcp', version('mcp'))"
```

Expected:

```text
google-adk 2.7.1
mcp 1.29.0
```

## Deferred Google Cloud runtime

Automated readiness requires no Google Cloud credentials. The live Gemini acceptance test remains deferred until the intended hackathon credit arrangement is available for a dedicated CineScout AI project.

The planned environment is:

```text
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-cinescout-project-id
GOOGLE_CLOUD_LOCATION=global
CINESCOUT_MODEL=gemini-3.6-flash
PARALLEL_MCP_URL=https://search.parallel.ai/mcp
```

The later Phase 2 credentialled acceptance test must demonstrate one complete five-stage execution in which the Evidence Verifier invokes Parallel at runtime and the resulting evidence reaches the Production Risk Agent and Report Synthesiser with sources and uncertainty preserved.

## Security

Secrets do not belong in source control. The repository ignores `.env`, local virtual environments, service-account JSON files and common generated artefacts. Production credentials will later be managed through Google Secret Manager and workload identity rather than committed files.

## Licence

This project is licensed under the MIT License. See [`LICENSE`](LICENSE).
