# Purpose: validate CineScout AI Phase 1 locally at no cost and without Codespaces.
$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Title,
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )

    Write-Host "`n--- $Title ---"
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Title failed with exit code $LASTEXITCODE."
    }
}

Write-Host "============================================================"
Write-Host "CINESCOUT AI - PHASE 1 LOCAL READINESS"
Write-Host "============================================================"

Write-Host "`n--- ENVIRONMENT ---"
if (-not $env:VIRTUAL_ENV) {
    throw "No active virtual environment was detected. Activate .venv before running readiness checks."
}
Write-Host "VIRTUAL_ENV=$env:VIRTUAL_ENV"

$PythonVersion = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($LASTEXITCODE -ne 0) {
    throw "Python could not be executed from the active virtual environment."
}

$Version = [version]$PythonVersion
if ($Version -lt [version]"3.11" -or $Version -ge [version]"3.14") {
    throw "Unsupported Python version $PythonVersion. Use Python 3.11, 3.12 or 3.13; Python 3.12 is recommended."
}

Write-Host "PYTHON_VERSION=$PythonVersion"
python --version

Invoke-Step "COMPILE" { python -m compileall -q app scripts tests }
Invoke-Step "RUFF" { python -m ruff check app scripts tests }
Invoke-Step "PYTEST" { python -m pytest -q }
Invoke-Step "REPOSITORY CONTRACT" { python scripts/check_phase1.py }

Write-Host "`n============================================================"
Write-Host "PHASE1_LOCAL_READINESS=PASS"
Write-Host "============================================================"
