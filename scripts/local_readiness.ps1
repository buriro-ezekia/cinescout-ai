# Purpose: validate CineScout AI Phase 1 locally without using Codespaces or paid API calls.
$ErrorActionPreference = "Stop"

Write-Host "============================================================"
Write-Host "CINESCOUT AI - PHASE 1 LOCAL READINESS"
Write-Host "============================================================"

Write-Host "`n--- PYTHON ---"
python --version

Write-Host "`n--- COMPILE ---"
python -m compileall -q app scripts tests

Write-Host "`n--- RUFF ---"
python -m ruff check app scripts tests

Write-Host "`n--- PYTEST ---"
python -m pytest -q

Write-Host "`n--- REPOSITORY CONTRACT ---"
python scripts/check_phase1.py

Write-Host "`n============================================================"
Write-Host "PHASE1_LOCAL_READINESS=PASS"
Write-Host "============================================================"
