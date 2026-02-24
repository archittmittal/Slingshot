# Start VIDYA OS Frontend (PowerShell)
# Run this from the D:\Slingshot directory

Write-Host "=== VIDYA OS Frontend ===" -ForegroundColor Cyan
Push-Location frontend
Write-Host "Starting React dev server on http://localhost:5173" -ForegroundColor Green
npm run dev
Pop-Location
