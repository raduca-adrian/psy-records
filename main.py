#!/usr/bin/env python3
"""
Entry point for Psychological Records (packaged build).
Launches the unified single-window application.
"""
import sys
from src.simple_main import main as app_main

if __name__ == "__main__":
    sys.exit(app_main())
