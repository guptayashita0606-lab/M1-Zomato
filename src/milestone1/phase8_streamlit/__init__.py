"""
Phase 8 - Streamlit Deployment

Single-process Python deployment path replicating CLI/API flow.
"""

from .app import main
from .theme import get_theme_config

__all__ = ["main", "get_theme_config"]
