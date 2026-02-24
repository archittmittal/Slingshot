# Start VIDYA OS Backend (PowerShell)
# Run this from the D:\Slingshot directory

Write-Host "=== VIDYA OS Backend ===" -ForegroundColor Cyan

Push-Location backend

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[1/3] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate and install
Write-Host "[2/3] Installing dependencies..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q

# Copy .env if not exists
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[INFO] Created .env from .env.example — edit if needed" -ForegroundColor Gray
}

Write-Host "[3/3] Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Gray
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Pop-Location
