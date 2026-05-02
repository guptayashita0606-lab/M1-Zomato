#!/usr/bin/env python3
"""
Streamlit app entry point for deployment.
This file serves as the main entry point for Streamlit Community Cloud deployment.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from milestone1.phase8_streamlit.app import main

if __name__ == "__main__":
    main()
