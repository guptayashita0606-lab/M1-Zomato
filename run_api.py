#!/usr/bin/env python3
"""
Entry point for running the FastAPI server.
"""

import uvicorn
from milestone1.phase6_api import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
