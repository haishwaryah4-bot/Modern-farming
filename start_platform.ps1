# AgriSense AI - Automated PowerShell Launcher
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "   AGRISENSE AI - SMART FARMING PLATFORM AUTOMATIC LAUNCHER" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting FastAPI Backend and Streamlit 3D Portal automatically..." -ForegroundColor Cyan
Write-Host "Opening browser at http://localhost:8501 ..." -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot
& "C:\msys64\ucrt64\bin\python.exe" main_runner.py
