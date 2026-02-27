# Start VIDYA OS 2.0 Backend (PowerShell)
# Run this from the D:\Slingshot directory

Write-Host "=== VIDYA OS 2.0 · Agentic Engine ===" -ForegroundColor Magenta

Push-Location backend

# Activate and start
if (Test-Path "venv") {
    Write-Host "[1/2] Activating Sovereign Environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

Write-Host "[2/2] Starting Sovereign AI Engine on http://localhost:8000" -ForegroundColor Green
Write-Host "Engine: Transformers + ROCm Acceleration" -ForegroundColor Gray
Write-Host "Interactive Docs: http://localhost:8000/docs" -ForegroundColor Gray

# Use app.main:app for modular structure
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Pop-Location
