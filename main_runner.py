"""
AgriSense AI - Unified Platform Auto-Launcher.
Runs the FastAPI Backend (Port 8000) and the Streamlit 3D Portal (Port 8501)
concurrently, and automatically opens your web browser!
"""

import sys
import os
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

# Paths & Python Executable
BASE_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable


def run_fastapi():
    """Runs FastAPI backend on port 8000."""
    print("🚀 [1/2] Starting FastAPI Backend on http://localhost:8000 ...")
    env = os.environ.copy()
    subprocess.run([PYTHON_EXE, "server.py"], cwd=str(BASE_DIR), env=env)


def run_streamlit():
    """Runs Streamlit portal on port 8501."""
    print("🌾 [2/2] Starting Streamlit 3D Agriculture Portal on http://localhost:8501 ...")
    env = os.environ.copy()
    subprocess.run(
        [
            PYTHON_EXE,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port",
            "8501",
            "--server.headless",
            "false",
        ],
        cwd=str(BASE_DIR),
        env=env,
    )


def open_browser():
    """Automatically launches default web browser once servers are up."""
    time.sleep(3)
    print("🌐 Automatically opening AgriSense AI Platform in your default browser...")
    webbrowser.open("http://localhost:8501")


def main():
    print("=" * 75)
    print("   🌾 AGRISENSE AI - NATIONAL SMART AGRICULTURE PLATFORM (AUTO-RUNNER)")
    print("=" * 75)

    # Launch browser thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Launch FastAPI in background thread
    t_api = threading.Thread(target=run_fastapi, daemon=True)
    t_api.start()

    # Launch Streamlit in main thread
    time.sleep(1)
    run_streamlit()


if __name__ == "__main__":
    main()
