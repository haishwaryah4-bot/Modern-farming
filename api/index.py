"""
Vercel Serverless Function Entrypoint for AgriSense AI.
Exposes both `app` and `handler` for seamless ASGI routing on Vercel.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from server import app

# Vercel ASGI runtime handler
handler = app
