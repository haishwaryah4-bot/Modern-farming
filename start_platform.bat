@echo off
title AgriSense AI - Smart Farming Platform Launcher
color 0A

echo ======================================================================
echo    AGRISENSE AI - SMART FARMING PLATFORM AUTOMATIC LAUNCHER
echo ======================================================================
echo.
echo Starting FastAPI Backend and Streamlit 3D Portal automatically...
echo Opening browser at http://localhost:8501 ...
echo.

cd /d "%~dp0"
"C:\msys64\ucrt64\bin\python.exe" main_runner.py

pause
